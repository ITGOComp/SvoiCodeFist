function initMap() {
  DG.then(function() {
    var map = DG.map('traffic-map', {
      center: [54.7818, 32.0401],
      zoom: 11,
      scrollWheelZoom: false
    });

    var trafficLayer = DG.featureGroup();
    var incidentsLayer = DG.featureGroup();
    var patrolLayer = DG.featureGroup();
    var camerasLayer = DG.featureGroup();
  var speedLayer = DG.featureGroup();

    // Load traffic jams from API
    fetch('/api/traffic/')
      .then(function(res) { return res.json(); })
      .then(function(payload) {
        (payload.traffic || []).forEach(function(traffic) {
          var coords = traffic.coordinates;
          if (Array.isArray(coords) && coords.length >= 2) {
            var lat = parseFloat(coords[0]);
            var lon = parseFloat(coords[1]);
            if (!isFinite(lat) || !isFinite(lon)) return;
            
            var color = '#FF6B35'; // Default orange for traffic
            if (traffic.severity === 'high') color = '#FF0000';
            else if (traffic.severity === 'low') color = '#FFA500';
            
            var polyline = DG.polyline([[lat, lon], [lat + 0.001, lon + 0.001]], {
              color: color,
              weight: 4,
              opacity: 0.8
            }).bindPopup(formatTrafficDescription(traffic));
            trafficLayer.addLayer(polyline);
          }
        });
      })
      .catch(function(err) { console.error('Failed to load traffic', err); });

    fetch('/api/incidents/')
      .then(function(res) { return res.json(); })
      .then(function(payload) {
        (payload.incidents || []).forEach(function(incident) {
          var coords = incident.coordinates;
          if (typeof coords === 'string') {
            try { coords = JSON.parse(coords); } catch (_) { coords = null; }
          }
          if (Array.isArray(coords) && coords.length === 2) {
            var lat = parseFloat(coords[0]);
            var lon = parseFloat(coords[1]);
            if (!isFinite(lat) || !isFinite(lon)) return;
            var marker = DG.marker([lat, lon]).bindPopup(
              '<b>' + incident.title + '</b><br>' + (incident.description || '')
            );
            incidentsLayer.addLayer(marker);
          }
        });
      })
      .catch(function(err) { console.error('Failed to load incidents', err); });

    // Load patrols from API
    fetch('/api/patrols/')
      .then(function(res) { return res.json(); })
      .then(function(payload) {
        (payload.patrols || []).forEach(function(patrol) {
          var coords = patrol.coordinates;
          if (Array.isArray(coords) && coords.length >= 2) {
            var lat = parseFloat(coords[0]);
            var lon = parseFloat(coords[1]);
            if (!isFinite(lat) || !isFinite(lon)) return;
            
            var circle = DG.circle([lat, lon], {
              radius: patrol.radius_m || 100,
              color: '#00A8A8',
              fillColor: '#00A8A8',
              fillOpacity: 0.5
            }).bindPopup('<b>' + patrol.title + '</b><br>' + (patrol.description || ''));
            patrolLayer.addLayer(circle);
          }
        });
      })
      .catch(function(err) { console.error('Failed to load patrols', err); });

    // Load cameras from API
    fetch('/api/cameras/')
      .then(function(res) { return res.json(); })
      .then(function(payload) {
        (payload.cameras || []).forEach(function(cam) {
          var coords = cam.coordinates;
          if (typeof coords === 'string') {
            try { coords = JSON.parse(coords); } catch (_) { coords = null; }
          }
          if (Array.isArray(coords) && coords.length === 2) {
            var lat = parseFloat(coords[0]);
            var lon = parseFloat(coords[1]);
            if (!isFinite(lat) || !isFinite(lon)) return;
            var marker = DG.marker([lat, lon], {
              icon: DG.icon({
                iconUrl: 'https://maps.api.2gis.ru/2.0/img/marker.png',
                iconSize: [25, 41]
              })
            }).bindPopup('<b>' + (cam.name || 'Камера') + '</b><br>' + (cam.description || ''));
            camerasLayer.addLayer(marker);
          }
        });
      })
      .catch(function(err) { console.error('Failed to load cameras', err); });

    // Speed mode demo layer (optional generated sample based on traffic)
    fetch('/api/traffic/')
      .then(function(res) { return res.json(); })
      .then(function(payload) {
        (payload.traffic || []).forEach(function(traffic) {
          var coords = traffic.coordinates;
          if (Array.isArray(coords) && coords.length >= 2) {
            var lat = parseFloat(coords[0]);
            var lon = parseFloat(coords[1]);
            if (!isFinite(lat) || !isFinite(lon)) return;
            // derive allowed speed suggestion by severity
            var speed = 60;
            if (traffic.severity === 'high') speed = 30;
            else if (traffic.severity === 'medium') speed = 50;
            else if (traffic.severity === 'low') speed = 70;
            var color = speed <= 30 ? '#d32f2f' : (speed <= 50 ? '#f57c00' : '#388e3c');
            var circle = DG.circle([lat, lon], {
              radius: 120,
              color: color,
              fillColor: color,
              fillOpacity: 0.25
            }).bindPopup('<b>Режим скорости:</b> ' + speed + ' км/ч');
            speedLayer.addLayer(circle);
          }
        });
      })
      .catch(function(err) { console.error('Failed to build speed mode', err); });

    // Add default layers
    trafficLayer.addTo(map);
    incidentsLayer.addTo(map);

    document.querySelectorAll('.map-filter').forEach(function(filter) {
      filter.addEventListener('click', function() {
        var layerName = this.dataset.layer;
        this.classList.toggle('active');

        var layer = null;
        if (layerName === 'traffic') layer = trafficLayer;
        else if (layerName === 'incidents') layer = incidentsLayer;
        else if (layerName === 'patrol') layer = patrolLayer;
        else if (layerName === 'cameras') layer = camerasLayer;
        else if (layerName === 'speed') layer = speedLayer;

        if (layer) {
          if (this.classList.contains('active')) {
            layer.addTo(map);
          } else {
            map.removeLayer(layer);
          }
        }
      });
    });

    setTimeout(function() {
      map.invalidateSize();
    }, 100);
  });
}

try {
  document.getElementById('contact-form').addEventListener('submit', function(e) {
    e.preventDefault();
    var form = this;
    var formData = new FormData(form);
    fetch('/appeal/', {
      method: 'POST',
      headers: {
        'X-Requested-With': 'XMLHttpRequest'
      },
      body: formData
    }).then(function(res) {
      if (!res.ok) return res.json().then(function(err){ throw err; });
      return res.json();
    }).then(function() {
      alert('Спасибо! Ваше обращение отправлено.');
      form.reset();
    }).catch(function(err) {
      console.error('Ошибка отправки обращения', err);
      alert('Не удалось отправить обращение. Проверьте поля и попробуйте снова.');
    });
  });
} catch (e) {}

document.getElementById('hamburgerBtn').addEventListener('click', function() {
  const navMenu = document.getElementById('navMenu');
  navMenu.classList.toggle('active');
});

try {
  document.getElementById('loginBtn').addEventListener('click', function(){
    window.location.href = '/accounts/login/';
  });
} catch (e) {}

document.addEventListener('DOMContentLoaded', function() {
  initMap();
  initChat();
});

function formatTrafficDescription(traffic) {
  var severityHuman = {
    'low': 'низкая загруженность',
    'medium': 'средняя загруженность',
    'high': 'сильная загруженность'
  }[traffic.severity] || 'загруженность';
  var title = traffic.title || 'Пробка';
  return '<b>' + title + '</b><br>' + severityHuman + (traffic.description ? ('<br>' + traffic.description) : '');
}

// Enhance traffic popups to human-friendly text
(function(){
  var _fetch = window.fetch;
  window.fetch = function(){ return _fetch.apply(this, arguments).then(function(res){ return res; }); };
})();

function initChat() {
  var messagesEl = document.getElementById('chat-messages');
  var inputEl = document.getElementById('chat-text');
  var subjectEl = document.getElementById('chat-subject');
  var sendBtn = document.getElementById('chat-send');
  var authHint = document.getElementById('chat-auth-hint');
  if (!messagesEl || !sendBtn) return;

  function loadMessages() {
    fetch('/api/chat/messages/')
      .then(function(r){return r.json();})
      .then(function(payload){
        messagesEl.innerHTML = '';
        (payload.messages || []).forEach(function(m){
          var div = document.createElement('div');
          div.className = 'chat-message ' + (m.sender === 'admin' ? 'admin' : 'user');
          div.innerHTML = '<span class="sender">' + (m.sender === 'admin' ? 'Админ' : 'Вы') + ':</span> ' + m.content;
          messagesEl.appendChild(div);
        });
        messagesEl.scrollTop = messagesEl.scrollHeight;
        authHint.style.display = payload.is_authenticated ? 'none' : 'block';
      })
      .catch(function(err){ console.error('Chat load failed', err); });
  }

  loadMessages();
  setInterval(loadMessages, 5000);

  sendBtn.addEventListener('click', function(){
    var text = (inputEl.value || '').trim();
    var subject = (subjectEl.value || '').trim();
    if (!text) return;
    fetch('/api/chat/send/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ content: text, subject: subject })
    }).then(function(r){ return r.json(); })
      .then(function(){ inputEl.value=''; loadMessages(); })
      .catch(function(err){ console.error('Chat send failed', err); });
  });
}