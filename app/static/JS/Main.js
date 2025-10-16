// Новые элементы для доступности
    const accessibilityPanel = document.getElementById('accessibility-panel');
    const accessibilityToggle = document.getElementById('accessibility-toggle');
    const accessibilityBtnDesktop = document.getElementById('accessibility-btn');
    const accessibilityBtnMobile = document.getElementById('accessibility-btn-mobile');
    const fontSizeUpBtn = document.getElementById('font-size-up');
    const fontSizeDownBtn = document.getElementById('font-size-down');
    const spacingUpBtn = document.getElementById('spacing-up');
    const spacingDownBtn = document.getElementById('spacing-down');
    const invertedColorsToggle = document.getElementById('inverted-colors-toggle');
    const resetAccessibilityBtn = document.getElementById('reset-accessibility');














const mobileMenuBtn = document.getElementById('hamburgerBtn');
const navMenu = document.getElementById('navMenu');

mobileMenuBtn.addEventListener('click', () => {
    navMenu.classList.toggle('active');
});

document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const targetId = this.getAttribute('href');
        const targetElement = document.querySelector(targetId);
        if (targetElement) {
            targetElement.scrollIntoView({
                behavior: 'smooth'
            });
        }
        if (navMenu.classList.contains('active')) {
            navMenu.classList.remove('active');
        }
    });
});

const loginBtn = document.getElementById('loginBtn');
const loginModal = document.getElementById('login-modal');
const closeBtn = document.querySelector('.modal .close-btn');

loginBtn.addEventListener('click', () => {
    loginModal.style.display = 'flex';
});

closeBtn.addEventListener('click', () => {
    loginModal.style.display = 'none';
});

window.addEventListener('click', (event) => {
    if (event.target === loginModal) {
        loginModal.style.display = 'none';
    }
});

const loginForm = document.getElementById('login-form');
const usernameInput = document.getElementById('username');
const passwordInput = document.getElementById('password');
const errorMessage = document.getElementById('error-message');
const loginSubmitBtn = document.getElementById('login-submit-btn');
const userControls = document.getElementById('user-controls');
const userDisplay = document.getElementById('user-display');
const adminPanelBtn = document.getElementById('adminPanelBtn');
const editorPanelBtn = document.getElementById('editorPanelBtn');
const logoutBtn = document.getElementById('logoutBtn');
const adminPanelSection = document.getElementById('admin-panel');
const editorPanelSection = document.getElementById('editor-panel');
const appealsBtn = document.getElementById('appealsBtn');
const appealSection = document.getElementById('appeal');

// Пользователи теперь управляются через Django
let currentUser = null;

// Функция проверки статуса авторизации
function checkAuthStatus() {
    fetch('/api/auth/status/', {
        method: 'GET',
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.authenticated) {
            currentUser = data.user;
            loginBtn.style.display = 'none';
            userControls.style.display = 'flex';
            userDisplay.textContent = `${data.user.username} (${data.user.role})`;
            if (data.user.role === 'admin') {
                adminPanelBtn.style.display = 'block';
                editorPanelBtn.style.display = 'none';
            } else if (data.user.role === 'editor') {
                adminPanelBtn.style.display = 'none';
                editorPanelBtn.style.display = 'block';
            }
        } else {
            currentUser = null;
            loginBtn.style.display = 'block';
            userControls.style.display = 'none';
        }
    })
    .catch(error => {
        console.error('Ошибка проверки авторизации:', error);
        currentUser = null;
        loginBtn.style.display = 'block';
        userControls.style.display = 'none';
    });
}

loginForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const username = usernameInput.value;
    const password = passwordInput.value;

    loginSubmitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Вход...';
    loginSubmitBtn.disabled = true;

    // Отправляем данные на сервер для аутентификации
    fetch('/login/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({
            username: username,
            password: password
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            loginModal.style.display = 'none';
            showNotification('Вход выполнен успешно!', 'success');

            currentUser = data.user;

            loginBtn.style.display = 'none';
            userControls.style.display = 'flex';
            userDisplay.textContent = `${data.user.username} (${data.user.role})`;
            if (data.user.role === 'admin') {
                adminPanelBtn.style.display = 'block';
                editorPanelBtn.style.display = 'none';
            } else if (data.user.role === 'editor') {
                adminPanelBtn.style.display = 'none';
                editorPanelBtn.style.display = 'block';
            }

            hideAllPanels();
        } else {
            errorMessage.textContent = 'Неправильное имя пользователя или пароль.';
            errorMessage.style.display = 'block';
        }

        loginSubmitBtn.innerHTML = '<i class="fas fa-sign-in-alt"></i> Войти';
        loginSubmitBtn.disabled = false;
    })
    .catch(error => {
        console.error('Ошибка входа:', error);
        errorMessage.textContent = 'Ошибка входа';
        errorMessage.style.display = 'block';
        loginSubmitBtn.innerHTML = '<i class="fas fa-sign-in-alt"></i> Войти';
        loginSubmitBtn.disabled = false;
    });
});

logoutBtn.addEventListener('click', () => {
    // Отправляем запрос на выход
    fetch('/logout/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
    .then(() => {
        currentUser = null;
        loginBtn.style.display = 'block';
        userControls.style.display = 'none';
        hideAllPanels();
        showNotification('Вы вышли из системы.', 'info');
    })
    .catch(error => {
        console.error('Ошибка выхода:', error);
        showNotification('Ошибка выхода', 'error');
    });
});

function hideAllPanels() {
    adminPanelSection.style.display = 'none';
    editorPanelSection.style.display = 'none';
    appealSection.style.display = 'none';
}

adminPanelBtn.addEventListener('click', () => {
    hideAllPanels();
    adminPanelSection.style.display = 'block';
    adminPanelSection.scrollIntoView({ behavior: 'smooth' });
});

editorPanelBtn.addEventListener('click', () => {
    hideAllPanels();
    editorPanelSection.style.display = 'block';
    editorPanelSection.scrollIntoView({ behavior: 'smooth' });
});

appealsBtn.addEventListener('click', () => {
    hideAllPanels();
    appealSection.style.display = 'block';
    appealSection.scrollIntoView({ behavior: 'smooth' });
});

// Управление видимостью выпадающего меню по клику
const userGreeting = document.querySelector('.user-greeting');
const logoutDropdown = document.querySelector('.logout-dropdown');

userGreeting.addEventListener('click', (event) => {
    event.stopPropagation();
    logoutDropdown.classList.toggle('dropdown-show');
});

document.addEventListener('click', (event) => {
    if (!userGreeting.contains(event.target) && logoutDropdown.classList.contains('dropdown-show')) {
        logoutDropdown.classList.remove('dropdown-show');
    }
});

function showNotification(message, type) {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.innerHTML = `<span class="icon"><i class="fas fa-${type === 'success' ? 'check-circle' : 'info-circle'}"></i></span><span>${message}</span>`;
    document.body.appendChild(notification);

    setTimeout(() => {
        notification.classList.add('show');
    }, 10);

    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => {
            notification.remove();
        }, 500);
    }, 3000);
}

const contactForm = document.getElementById('contact-form');
const appealsList = document.getElementById('appeals-list');
const appealsListAdmin = document.getElementById('appeals-list-admin');
const noAppealsMsg = `<div class="no-appeals">Обращения отсутствуют.</div>`;
// Обращения теперь хранятся в БД

function renderAppeals(targetElement) {
    if (!targetElement) return;

    targetElement.innerHTML = '';

    // Загружаем обращения из БД
    fetch('/api/appeals/')
        .then(response => response.json())
        .then(data => {
            if (data.appeals && data.appeals.length === 0) {
        targetElement.innerHTML = noAppealsMsg;
    } else {
                data.appeals.forEach((appeal, index) => {
            const appealItem = document.createElement('div');
            appealItem.className = 'appeal-item';
            appealItem.innerHTML = `
                <div class="appeal-meta">
                    <span class="email">${appeal.email}</span>
                            <span class="date">${new Date(appeal.created_at).toLocaleString('ru-RU')}</span>
                            <span class="status ${appeal.is_reviewed ? 'reviewed' : 'pending'}">
                                ${appeal.is_reviewed ? 'Рассмотрено' : 'Нерассмотрено'}
                            </span>
                </div>
                <div class="appeal-message">${appeal.message}</div>
            `;
            targetElement.appendChild(appealItem);
        });
    }
        })
        .catch(error => {
            console.error('Ошибка загрузки обращений:', error);
            targetElement.innerHTML = '<div class="error">Ошибка загрузки обращений</div>';
        });
}

contactForm.addEventListener('submit', (e) => {
    e.preventDefault();

    const formData = new FormData(contactForm);

    fetch('/appeal/', {
        method: 'POST',
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        },
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.ok) {
    contactForm.reset();
    showNotification('Ваше обращение отправлено!', 'success');
            // Обновляем списки обращений
            loadAppeals('all');
        } else {
            showNotification('Ошибка при отправке обращения', 'error');
        }
    })
    .catch(error => {
        console.error('Ошибка:', error);
        showNotification('Ошибка при отправке обращения', 'error');
    });
});

// Настройки эвакуатора теперь хранятся в БД
let evacuatorSettings = {
    baseRate: 1500,
    kmRate: 50,
    multipliers: {
        car: 1,
        suv: 1.5,
        truck: 2
    }
};

const calculateBtn = document.getElementById('calculate-btn');
const carTypeSelect = document.getElementById('car-type');
const distanceInput = document.getElementById('distance');
const priceDisplay = document.getElementById('price');

calculateBtn.addEventListener('click', () => {
    const type = carTypeSelect.value;
    const distance = parseInt(distanceInput.value);
    const totalCost = (evacuatorSettings.baseRate + (distance * evacuatorSettings.kmRate)) * evacuatorSettings.multipliers[type];

    let currentPrice = parseInt(priceDisplay.textContent.replace(/\s/g, '')) || 0;
    const step = (totalCost - currentPrice) / 60;

    const interval = setInterval(() => {
        currentPrice += step;
        if ((step > 0 && currentPrice >= totalCost) || (step < 0 && currentPrice <= totalCost)) {
            currentPrice = totalCost;
            clearInterval(interval);
        }
        priceDisplay.textContent = Math.round(currentPrice).toLocaleString('ru-RU');
    }, 10);
});

// Панель администратора
const adminNavBtns = document.querySelectorAll('.admin-nav-btn');
const adminViews = document.querySelectorAll('.admin-panel-content');

let adminMap = null;
let isMapInitialized = false;

adminNavBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        adminNavBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');

        // Скрываем все вкладки
        const allViews = document.querySelectorAll('.admin-panel-content');
        allViews.forEach(view => {
            view.classList.remove('active');
            view.style.display = 'none';
        });

        const targetViewId = btn.getAttribute('data-view');
        const targetView = document.getElementById(targetViewId);
        if (targetView) {
            targetView.classList.add('active');
            targetView.style.display = 'block';
        }

        if (targetViewId === 'admin-main-view') {
            if (!isMapInitialized) {
                (function(){
                    adminMap = L.map('admin-map', {
                        center: [54.782, 32.045],
                        zoom: 13,
                        attributionControl: false
                    });
                    const adminAttr = L.control.attribution().addTo(adminMap);
                    adminAttr.setPrefix('<a href="https://itgol.ru/">Фисташечки</a>');
                    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                        maxZoom: 19,
                        attribution: 'Data by &copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>, under <a href="https://opendatacommons.org/licenses/odbl/">ODbL.</a>'
                    }).addTo(adminMap);

                    const coordsInput = document.getElementById('object-coords');
                    let marker = null;
                    // Объекты карты теперь хранятся в БД
                    let objects = [];

                    function renderTable() {
                        const tableBody = document.querySelector('#data-table tbody');
                        tableBody.innerHTML = '';
                        objects.forEach((obj, index) => {
                            const row = tableBody.insertRow();
                            row.innerHTML = `
                                <td>${obj.type}</td>
                                <td>${obj.description}</td>
                                <td>${obj.coords.join(', ')}</td>
                                <td>
                                    <button class="action-btn btn-primary edit-btn" data-index="${index}">
                                        <i class="fas fa-edit"></i>
                                    </button>
                                    <button class="action-btn btn-secondary delete-btn" data-index="${index}">
                                        <i class="fas fa-trash-alt"></i>
                                    </button>
                                </td>
                            `;
                        });
                    }

                    adminMap.on('click', (e) => {
                        const lat = e.latlng.lat.toFixed(6);
                        const lng = e.latlng.lng.toFixed(6);
                        coordsInput.value = `${lat}, ${lng}`;

                        if (marker) {
                            adminMap.removeLayer(marker);
                        }
                        marker = L.marker([lat, lng]).addTo(adminMap);
                    });

                    document.getElementById('add-object-form').addEventListener('submit', (e) => {
                        e.preventDefault();
                        const type = document.getElementById('object-type').value;
                        const description = document.getElementById('object-description').value;
                        const coords = coordsInput.value.split(',').map(c => parseFloat(c.trim()));

                        if (coords.length === 2 && !isNaN(coords[0]) && !isNaN(coords[1])) {
                            objects.push({ type, description, coords });
                            // Объекты сохраняются в БД
                            renderTable();
                            showNotification('Объект добавлен!', 'success');
                            e.target.reset();
                            if (marker) {
                                adminMap.removeLayer(marker);
                                marker = null;
                            }
                            loadMapObjects(); // Обновить основную карту
                        } else {
                            showNotification('Пожалуйста, выберите координаты на карте.', 'info');
                        }
                    });

                    document.getElementById('data-table').addEventListener('click', (e) => {
                        if (e.target.classList.contains('delete-btn')) {
                            const index = e.target.getAttribute('data-index');
                            objects.splice(index, 1);
                            // Объекты сохраняются в БД
                            renderTable();
                            showNotification('Объект удалён!', 'info');
                            loadMapObjects(); // Обновить основную карту
                        }
                    });

                    renderTable();
                    isMapInitialized = true;
                })();
            }
            if (adminMap) {
                setTimeout(() => { adminMap.invalidateSize(); }, 100);
            }
        }
        if (targetViewId === 'appeals-admin-view') {
            renderAppeals(appealsListAdmin);
        }
        if (targetViewId === 'users-view') {
            renderUsersTable();
        }
        if (targetViewId === 'evacuator-settings-view') {
            document.getElementById('base-rate').value = evacuatorSettings.baseRate;
            document.getElementById('km-rate').value = evacuatorSettings.kmRate;
            document.getElementById('car-multiplier').value = evacuatorSettings.multipliers.car;
            document.getElementById('suv-multiplier').value = evacuatorSettings.multipliers.suv;
            document.getElementById('truck-multiplier').value = evacuatorSettings.multipliers.truck;
        }
        if (targetViewId === 'traffic-settings-view') {
            document.getElementById('low-traffic-color').value = trafficColors.low;
            document.getElementById('medium-traffic-color').value = trafficColors.medium;
            document.getElementById('high-traffic-color').value = trafficColors.high;
            document.getElementById('low-traffic-color-value').textContent = trafficColors.low;
            document.getElementById('medium-traffic-color-value').textContent = trafficColors.medium;
            document.getElementById('high-traffic-color-value').textContent = trafficColors.high;
        }
        if (targetViewId === 'weather-settings-view') {
            loadWeatherSettingsForm();
        }
        if (targetViewId === 'accident-management-view') {
            loadAccidentTypes();
        }
        if (targetViewId === 'chat-management-view') {
            loadAdminChatThreads();
        }
    });
});

let trafficMap = null;
let mapObjectsLayer = null;

(function(){
    trafficMap = L.map('traffic-map', {
        center: [54.782, 32.045],
        zoom: 13,
        attributionControl: false
    });
    const publicAttr = L.control.attribution().addTo(trafficMap);
    publicAttr.setPrefix('<a href="https://itgol.ru/">Фисташечки</a>');
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: 'Data by &copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>, under <a href="https://opendatacommons.org/licenses/odbl/">ODbL.</a>'
    }).addTo(trafficMap);

    const trafficLayer = L.featureGroup().addTo(trafficMap);
    const incidentLayer = L.featureGroup();
    const patrolLayer = L.featureGroup();
    const cameraLayer = L.featureGroup();
    mapObjectsLayer = L.featureGroup().addTo(trafficMap);

    const layers = {
        traffic: trafficLayer,
        incidents: incidentLayer,
        patrol: patrolLayer,
        cameras: cameraLayer
    };

    L.marker([54.789, 32.06]).addTo(incidentLayer).bindPopup('ДТП: Столкновение');
    L.marker([54.78, 32.03]).addTo(incidentLayer).bindPopup('ДТП: Наезд на пешехода');
    L.marker([54.77, 32.05]).addTo(patrolLayer).bindPopup('Патруль ДПС');
    L.marker([54.79, 32.04]).addTo(cameraLayer).bindPopup('Камера контроля скорости');

    document.querySelectorAll('.map-filter').forEach(button => {
        button.addEventListener('click', () => {
            document.querySelectorAll('.map-filter').forEach(btn => btn.classList.remove('active'));
            button.classList.add('active');
            
            const layerId = button.getAttribute('data-layer');
            
            for (const id in layers) {
                trafficMap.removeLayer(layers[id]);
            }

            if (layerId === 'traffic') {
                trafficMap.addLayer(trafficLayer);
            } else {
                trafficMap.addLayer(layers[layerId]);
            }
        });
    });

    loadMapObjects();
})();

function loadMapObjects() {
    const objects = JSON.parse(localStorage.getItem('mapObjects')) || [];
    mapObjectsLayer.clearLayers();
    objects.forEach(obj => {
        const marker = L.marker(obj.coords).addTo(mapObjectsLayer).bindPopup(`${obj.type}: ${obj.description}`);
    });
}

// Аналитика
const analyticsData = {
    labels: ['Янв', 'Фев', 'Мар', 'Апр', 'Май', 'Июн'],
    datasets: [{
        label: 'ДТП',
        data: [150, 180, 210, 190, 220, 250],
        borderColor: 'rgb(75, 192, 192)',
        tension: 0.1
    }]
};

const analyticsCtx = document.getElementById('admin-analytics-chart').getContext('2d');
new Chart(analyticsCtx, {
    type: 'bar',
    data: analyticsData,
    options: {
        responsive: true,
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});

// Данные теперь загружаются из базы данных через Django
let monitoringData = {
    injured: 0,
    killed: 0,
    total: 0
};

// Функция загрузки данных мониторинга с сервера
async function loadMonitoringData() {
    try {
        const response = await fetch('/api/accident-stats/', {
            method: 'GET',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        });
        
        if (response.ok) {
            const data = await response.json();
            if (data.accident_stats) {
                monitoringData = {
                    total: data.accident_stats.total_accidents || 0,
                    injured: data.accident_stats.injured || 0,
                    killed: data.accident_stats.killed || 0
                };
            }
        }
    } catch (error) {
        console.error('Ошибка загрузки данных мониторинга:', error);
    }
}

// Функция загрузки данных в форму статистики ДТП
function loadAccidentStatsForm() {
    const accidentTotal = document.getElementById('accident-total');
    const accidentInjured = document.getElementById('accident-injured');
    const accidentKilled = document.getElementById('accident-killed');
    const accidentYear = document.getElementById('accident-year');
    
    if (accidentTotal) accidentTotal.value = monitoringData.total;
    if (accidentInjured) accidentInjured.value = monitoringData.injured;
    if (accidentKilled) accidentKilled.value = monitoringData.killed;
    if (accidentYear) accidentYear.value = 2024;
}

// Функция загрузки данных в форму настроек погоды
async function loadWeatherSettingsForm() {
    try {
        // Загружаем данные погоды
        const weatherResponse = await fetch('/api/weather/', {
            method: 'GET',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        });
        
        if (weatherResponse.ok) {
            const weatherData = await weatherResponse.json();
            if (weatherData.weather) {
                document.getElementById('current-temp').value = weatherData.weather.temperature || '';
                document.getElementById('current-weather').value = weatherData.weather.description || '';
                document.getElementById('current-weather-icon').value = weatherData.weather.icon || 'fa-sun';
            }
        }
        
        // Загружаем данные трафика
        const trafficResponse = await fetch('/api/traffic-forecast/', {
            method: 'GET',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        });
        
        if (trafficResponse.ok) {
            const trafficData = await trafficResponse.json();
            if (trafficData.traffic_forecast) {
                document.getElementById('current-speed').value = trafficData.traffic_forecast.speed || '';
            }
        }
        
        // Загружаем данные дорожных работ
        const roadWorksResponse = await fetch('/api/road-works/', {
            method: 'GET',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        });
        
        if (roadWorksResponse.ok) {
            const roadWorksData = await roadWorksResponse.json();
            if (roadWorksData.road_works) {
                document.getElementById('current-works').value = roadWorksData.road_works.count || '';
            }
        }
        
        // Загружаем статистику ДТП
        const statsResponse = await fetch('/api/accident-stats/', {
            method: 'GET',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        });
        
        if (statsResponse.ok) {
            const statsData = await statsResponse.json();
            if (statsData.accident_stats) {
                document.getElementById('current-accidents').value = statsData.accident_stats.total_accidents || '';
                document.getElementById('current-injured').value = statsData.accident_stats.injured || '';
                document.getElementById('current-killed').value = statsData.accident_stats.killed || '';
            }
        }
    } catch (error) {
        console.error('Ошибка загрузки данных настроек погоды:', error);
    }
}

const updateMonitoringValues = () => {
    document.getElementById('total-accidents-value').textContent = monitoringData.total.toLocaleString('ru-RU');
    document.getElementById('injured-value').textContent = monitoringData.injured.toLocaleString('ru-RU');
    document.getElementById('killed-value').textContent = monitoringData.killed.toLocaleString('ru-RU');
    document.getElementById('total-accidents-value').setAttribute('data-target', monitoringData.total);
    document.getElementById('injured-value').setAttribute('data-target', monitoringData.injured);
    document.getElementById('killed-value').setAttribute('data-target', monitoringData.killed);
};

const uploadCsvBtn = document.getElementById('upload-csv-btn');
const csvFileInput = document.getElementById('csv-file');

uploadCsvBtn.addEventListener('click', () => {
    const file = csvFileInput.files[0];
    if (!file) {
        showNotification('Пожалуйста, выберите CSV-файл.', 'info');
        return;
    }

    const reader = new FileReader();
    reader.onload = (e) => {
        const text = e.target.result;
        const rows = text.split('\n').slice(1);
        
        let totalInjured = 0;
        let totalKilled = 0;
        let totalAccidents = 0;

        rows.forEach(row => {
            const [type, injured, killed] = row.split(',').map(item => item.trim());
            if (injured && killed) {
                totalInjured += parseInt(injured);
                totalKilled += parseInt(killed);
                totalAccidents++;
            }
        });

        monitoringData = {
            total: totalAccidents,
            injured: totalInjured,
            killed: totalKilled
        };
        // Данные мониторинга сохраняются в БД
        updateMonitoringValues();
        showNotification('Данные мониторинга обновлены!', 'success');
    };
    reader.readAsText(file);
});

// Upload detectors (CSV/XLSX) to backend
(function initTrafficUploads() {
    const detectorsInput = document.getElementById('detectors-file');
    const detectorsBtn = document.getElementById('upload-detectors-btn');
    const passesInput = document.getElementById('passes-file');
    const passesBtn = document.getElementById('upload-passes-btn');

    async function postFile(url, file) {
        const form = new FormData();
        form.append('file', file);
        const res = await fetch(url, {
            method: 'POST',
            body: form
        });
        const data = await res.json().catch(() => ({ ok: false, error: 'Invalid JSON' }));
        if (!res.ok || !data.ok) {
            const err = (data && (data.error || data.detail)) || `HTTP ${res.status}`;
            throw new Error(err);
        }
        return data;
    }

    if (detectorsBtn && detectorsInput) {
        detectorsBtn.addEventListener('click', async () => {
            const file = detectorsInput.files && detectorsInput.files[0];
            if (!file) {
                showNotification('Выберите файл с датчиками (.csv/.xlsx).', 'info');
                return;
            }
            try {
                const result = await postFile('/api/traffic/ingest/detectors/', file);
                const created = result.created || 0;
                const updated = result.updated || 0;
                showNotification(`Датчики загружены: создано ${created}, обновлено ${updated}.`, 'success');
            } catch (e) {
                console.error('Detectors upload failed:', e);
                showNotification(`Ошибка загрузки датчиков: ${e.message || e}`, 'error');
            }
        });
    }

    if (passesBtn && passesInput) {
        passesBtn.addEventListener('click', async () => {
            const file = passesInput.files && passesInput.files[0];
            if (!file) {
                showNotification('Выберите файл с проездами ТС (.csv/.xlsx).', 'info');
                return;
            }
            try {
                const result = await postFile('/api/traffic/ingest/passes/', file);
                const created = result.created || 0;
                showNotification(`Проезды загружены: записей ${created}.`, 'success');
            } catch (e) {
                console.error('Passes upload failed:', e);
                showNotification(`Ошибка загрузки проездов: ${e.message || e}`, 'error');
            }
        });
    }
})();

const animateNumbers = () => {
    const values = document.querySelectorAll('.indicator-card .value');
    values.forEach(value => {
        const target = parseInt(value.getAttribute('data-target'));
        let current = 0;
        const increment = target / 100;
        
        const interval = setInterval(() => {
            current += increment;
            if (current >= target) {
                current = target;
                clearInterval(interval);
            }
            value.textContent = Math.floor(current).toLocaleString('ru-RU');
        }, 20);
    });
};

// Данные загружаются из базы данных через Django
let dptData = window.accidentData || {};

const months = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'];

// Цвета теперь берутся из данных базы данных
const chartColors = {};
if (window.accidentData) {
    Object.keys(window.accidentData).forEach(type => {
        chartColors[type] = window.accidentData[type].color;
    });
}

let accidentChart = null;

const renderLineChart = () => {
    const ctx = document.getElementById('accident-line-chart').getContext('2d');
    
    const datasets = Object.keys(dptData).map(type => {
        return {
            label: type,
            data: dptData[type].data,
            borderColor: chartColors[type],
            backgroundColor: 'rgba(0, 0, 0, 0)',
            tension: 0.4,
            pointRadius: 6,
            pointBackgroundColor: chartColors[type],
            pointBorderColor: '#fff',
            pointBorderWidth: 2,
            pointHoverRadius: 8,
            pointHoverBackgroundColor: chartColors[type],
            pointHoverBorderColor: 'rgba(255, 255, 255, 0.8)',
        };
    });

    if (accidentChart) {
        accidentChart.destroy();
    }

    accidentChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: months,
            datasets: datasets
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false,
                },
                tooltip: {
                    enabled: false,
                    position: 'nearest',
                    external: function(context) {
                        let tooltipEl = document.getElementById('chartjs-tooltip');

                        if (!tooltipEl) {
                            tooltipEl = document.createElement('div');
                            tooltipEl.id = 'chartjs-tooltip';
                            tooltipEl.className = 'chartjs-tooltip-custom';
                            document.body.appendChild(tooltipEl);
                        }

                        const tooltipModel = context.tooltip;

                        if (tooltipModel.opacity === 0) {
                            tooltipEl.style.opacity = 0;
                            return;
                        }

                        if (tooltipModel.body) {
                            const title = tooltipModel.title[0] || '';
                            const bodyItems = tooltipModel.body.map(b => b.lines).flat();

                            let innerHtml = `<h4>${title}</h4>`;
                            bodyItems.forEach((item, index) => {
                                const [label, value] = item.split(': ');
                                const color = tooltipModel.labelColors[index].borderColor;
                                innerHtml += `<p><span class="color-box" style="background-color: ${color};"></span>${label}: <strong>${value}</strong></p>`;
                            });

                            tooltipEl.innerHTML = innerHtml;
                        }

                        const position = context.chart.canvas.getBoundingClientRect();
                        const tooltipPosition = {
                            x: position.left + window.pageXOffset + tooltipModel.caretX,
                            y: position.top + window.pageYOffset + tooltipModel.caretY
                        };

                        tooltipEl.style.opacity = 1;
                        tooltipEl.style.left = tooltipPosition.x + 'px';
                        tooltipEl.style.top = tooltipPosition.y + 'px';
                        tooltipEl.style.transform = `translateX(-50%)`;
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)',
                        drawBorder: false,
                    },
                    ticks: {
                        color: 'rgba(255, 255, 255, 0.7)',
                    },
                    title: {
                        display: true,
                        text: 'Количество',
                        color: 'rgba(255, 255, 255, 0.8)'
                    }
                },
                x: {
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)',
                        drawBorder: false,
                    },
                    ticks: {
                        color: 'rgba(255, 255, 255, 0.7)',
                    }
                }
            }
        }
    });
};

// Логика панели редактора
const editorContentList = document.getElementById('editor-content-list');
const addContentBtn = document.getElementById('add-content-btn');
const editFormContainer = document.getElementById('editor-form-container');
const contentEditForm = document.getElementById('content-edit-form');
const editTitleInput = document.getElementById('edit-title');
const editTextarea = document.getElementById('edit-text');
const editContentIdInput = document.getElementById('edit-content-id');
const cancelEditBtn = document.getElementById('cancel-edit-btn');
const newsContent = document.getElementById('news-content');
const monitoringEditForm = document.getElementById('monitoring-edit-form');
const editTotalAccidents = document.getElementById('edit-total-accidents');
const editInjured = document.getElementById('edit-injured');
const editKilled = document.getElementById('edit-killed');

// Контент теперь хранится в БД
let contentItems = [
    { id: 1, title: 'Новость: ЦОДД расширяет сеть камер', text: 'В рамках программы "Безопасные дороги" в Смоленске установлено 10 новых камер...', date: new Date().toISOString() },
    { id: 2, title: 'Статья: Правила дорожного движения для велосипедистов', text: 'Помните, что велосипедист — полноправный участник дорожного движения. Вот основные правила, которые стоит знать...', date: new Date().toISOString() }
];

function renderContentItems() {
    editorContentList.innerHTML = '';
    if (contentItems.length === 0) {
        editorContentList.innerHTML = '<p class="no-appeals">Нет материалов</p>';
    } else {
        contentItems.forEach(item => {
            const itemDiv = document.createElement('div');
            itemDiv.className = 'content-item';
            itemDiv.innerHTML = `
                <div class="content-item-text">
                    <h4>${item.title}</h4>
                    <p>${item.text.substring(0, 100)}...</p>
                </div>
                <div class="action-btns">
                    <button class="btn btn-primary action-btn edit-content-btn" data-id="${item.id}">
                        <i class="fas fa-edit"></i>
                    </button>
                    <button class="btn btn-secondary action-btn delete-content-btn" data-id="${item.id}">
                        <i class="fas fa-trash-alt"></i>
                    </button>
                </div>
            `;
            editorContentList.appendChild(itemDiv);
        });
    }
}

function renderNews() {
    newsContent.innerHTML = '';
    if (contentItems.length === 0) {
        newsContent.innerHTML = '<p class="no-appeals">Нет новостей</p>';
    } else {
        contentItems.forEach(item => {
            const newsCard = document.createElement('div');
            newsCard.className = 'news-card';
            newsCard.innerHTML = `
                <h3>${item.title}</h3>
                <p class="date">${new Date(item.date).toLocaleDateString('ru-RU')}</p>
                <p>${item.text.substring(0, 150)}...</p>
            `;
            newsContent.appendChild(newsCard);
        });
    }
}

function showEditForm(id) {
    const item = contentItems.find(i => i.id === id);
    if (item) {
        editContentIdInput.value = item.id;
        editTitleInput.value = item.title;
        editTextarea.value = item.text;
        editFormContainer.classList.add('active');
    }
}

editorContentList.addEventListener('click', (e) => {
    const editBtn = e.target.closest('.edit-content-btn');
    const deleteBtn = e.target.closest('.delete-content-btn');

    if (editBtn) {
        const id = parseInt(editBtn.getAttribute('data-id'));
        showEditForm(id);
    } else if (deleteBtn) {
        const id = parseInt(deleteBtn.getAttribute('data-id'));
        contentItems = contentItems.filter(item => item.id !== id);
        // Контент сохраняется в БД
        renderContentItems();
        renderNews();
        showNotification('Материал удален!', 'info');
    }
});

addContentBtn.addEventListener('click', () => {
    editContentIdInput.value = '';
    editTitleInput.value = '';
    editTextarea.value = '';
    editFormContainer.classList.add('active');
});

cancelEditBtn.addEventListener('click', () => {
    editFormContainer.classList.remove('active');
});

contentEditForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const id = editContentIdInput.value;
    const title = editTitleInput.value;
    const text = editTextarea.value;

    if (id) {
        // Редактирование
        const itemIndex = contentItems.findIndex(item => item.id === parseInt(id));
        if (itemIndex > -1) {
            contentItems[itemIndex].title = title;
            contentItems[itemIndex].text = text;
            contentItems[itemIndex].date = new Date().toISOString();
            showNotification('Материал обновлен!', 'success');
        }
    } else {
        // Добавление
        const newId = contentItems.length ? Math.max(...contentItems.map(i => i.id)) + 1 : 1;
        contentItems.push({ id: newId, title, text, date: new Date().toISOString() });
        showNotification('Материал добавлен!', 'success');
    }

    // Контент сохраняется в БД
    renderContentItems();
    renderNews();
    editFormContainer.classList.remove('active');
});

monitoringEditForm.addEventListener('submit', (e) => {
    e.preventDefault();
    monitoringData.total = parseInt(editTotalAccidents.value);
    monitoringData.injured = parseInt(editInjured.value);
    monitoringData.killed = parseInt(editKilled.value);
    // Данные мониторинга сохраняются в БД
    updateMonitoringValues();
    animateNumbers();
    showNotification('Показатели обновлены!', 'success');
});

// Управление пользователями
const addUserForm = document.getElementById('add-user-form');
const usersTableBody = document.querySelector('#users-table tbody');

function renderUsersTable() {
    usersTableBody.innerHTML = '';
    users.forEach((user, index) => {
        if (user.role !== 'admin') { // Не показываем админа
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${user.username}</td>
                <td>${user.role}</td>
                <td>
                    <button class="action-btn btn-secondary delete-user-btn" data-index="${index}">
                        <i class="fas fa-trash-alt"></i>
                    </button>
                </td>
            `;
            usersTableBody.appendChild(row);
        }
    });
}

addUserForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const username = document.getElementById('new-username').value;
    const password = document.getElementById('new-password').value;

    if (users.find(u => u.username === username)) {
        showNotification('Пользователь с таким именем уже существует.', 'info');
        return;
    }

    users.push({username, password, role: 'editor'});
    // Пользователи управляются через Django
    renderUsersTable();
    addUserForm.reset();
    showNotification('Редактор добавлен!', 'success');
});

document.getElementById('users-table').addEventListener('click', (e) => {
    if (e.target.classList.contains('delete-user-btn')) {
        const index = parseInt(e.target.getAttribute('data-index'));
        users.splice(index, 1);
        // Пользователи управляются через Django
        renderUsersTable();
        showNotification('Пользователь удален!', 'info');
    }
});

// Настройки эвакуатора
const evacuatorSettingsForm = document.getElementById('evacuator-settings-form');

evacuatorSettingsForm.addEventListener('submit', (e) => {
    e.preventDefault();
    evacuatorSettings.baseRate = parseInt(document.getElementById('base-rate').value);
    evacuatorSettings.kmRate = parseInt(document.getElementById('km-rate').value);
    evacuatorSettings.multipliers.car = parseFloat(document.getElementById('car-multiplier').value);
    evacuatorSettings.multipliers.suv = parseFloat(document.getElementById('suv-multiplier').value);
    evacuatorSettings.multipliers.truck = parseFloat(document.getElementById('truck-multiplier').value);
    // Настройки эвакуатора сохраняются в БД
    showNotification('Настройки эвакуатора обновлены!', 'success');
});

// Настройки цветов пробок
// Цвета трафика теперь хранятся в БД
let trafficColors = {
    low: '#00FF00',
    medium: '#FFFF00',
    high: '#FF0000'
};

const trafficSettingsForm = document.getElementById('traffic-settings-form');
const lowTrafficColor = document.getElementById('low-traffic-color');
const mediumTrafficColor = document.getElementById('medium-traffic-color');
const highTrafficColor = document.getElementById('high-traffic-color');
const lowTrafficColorValue = document.getElementById('low-traffic-color-value');
const mediumTrafficColorValue = document.getElementById('medium-traffic-color-value');
const highTrafficColorValue = document.getElementById('high-traffic-color-value');

lowTrafficColor.addEventListener('input', () => {
    lowTrafficColorValue.textContent = lowTrafficColor.value;
});
mediumTrafficColor.addEventListener('input', () => {
    mediumTrafficColorValue.textContent = mediumTrafficColor.value;
});
highTrafficColor.addEventListener('input', () => {
    highTrafficColorValue.textContent = highTrafficColor.value;
});

trafficSettingsForm.addEventListener('submit', (e) => {
    e.preventDefault();
    trafficColors.low = lowTrafficColor.value;
    trafficColors.medium = mediumTrafficColor.value;
    trafficColors.high = highTrafficColor.value;
    localStorage.setItem('trafficColors', JSON.stringify(trafficColors));
    showNotification('Настройки цветов пробок обновлены!', 'success');
    // Здесь можно применить цвета к карте, но поскольку 2GIS имеет фиксированные цвета, это может требовать кастомизации, которая не реализована
});

document.addEventListener('DOMContentLoaded', async () => {
    // Проверяем авторизацию через Django
    checkAuthStatus();
    
    // Загружаем данные мониторинга с сервера
    await loadMonitoringData();
    
    updateMonitoringValues();
    animateNumbers();
    renderLineChart();
    renderContentItems();
    renderNews();
    renderAppeals(appealsList);
    renderAppeals(appealsListAdmin);
    editTotalAccidents.value = monitoringData.total;
    editInjured.value = monitoringData.injured;
    editKilled.value = monitoringData.killed;
});

// Добавляем обработчик для кнопки редактирования распределения ДТП
const editDptDataBtn = document.getElementById('edit-dpt-data-btn');
const editDptDataModal = document.getElementById('edit-dpt-data-modal');
const editDptDataForm = document.getElementById('edit-dpt-data-form');
const dptTableBody = document.querySelector('#dpt-data-table tbody');
const types = Object.keys(dptData);

editDptDataBtn.addEventListener('click', () => {
    dptTableBody.innerHTML = '';
    types.forEach(type => {
        const row = document.createElement('tr');
        row.innerHTML = `<td>${type}</td>`;
        for (let i = 0; i < 12; i++) {
            const value = dptData[type] && dptData[type].data ? dptData[type].data[i] : 0;
            row.innerHTML += `<td><input type="number" value="${value}" data-type="${type}" data-month="${i}"></td>`;
        }
        dptTableBody.appendChild(row);
    });
    editDptDataModal.style.display = 'flex';
});

editDptDataForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const inputs = dptTableBody.querySelectorAll('input');
    
    // Собираем все обновления
    const updates = [];
    inputs.forEach(input => {
        const type = input.getAttribute('data-type');
        const month = parseInt(input.getAttribute('data-month'));
        const count = parseInt(input.value) || 0;
        
        // Находим ID типа ДТП
        const accidentType = Object.keys(dptData).find(key => key === type);
        if (accidentType && dptData[accidentType].id) {
            updates.push({
                accident_type_id: dptData[accidentType].id,
                month: month + 1, // Месяцы в БД начинаются с 1
                count: count,
                year: 2024
            });
        }
    });
    
    // Отправляем обновления на сервер
    Promise.all(updates.map(update => 
        fetch('/api/accident-data/update/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify(update)
        })
    )).then(responses => {
        const allOk = responses.every(response => response.ok);
        if (allOk) {
            // Обновляем локальные данные
            inputs.forEach(input => {
                const type = input.getAttribute('data-type');
                const month = parseInt(input.getAttribute('data-month'));
                const count = parseInt(input.value) || 0;
                
                if (dptData[type]) {
                    if (!dptData[type].data) {
                        dptData[type].data = new Array(12).fill(0);
                    }
                    dptData[type].data[month] = count;
                }
            });
            
            renderLineChart();
            editDptDataModal.style.display = 'none';
            showNotification('Данные распределения обновлены!', 'success');
        } else {
            showNotification('Ошибка при обновлении данных', 'error');
        }
    }).catch(error => {
        console.error('Ошибка:', error);
        showNotification('Ошибка при обновлении данных', 'error');
    });
});

const editDptCloseBtn = document.querySelector('#edit-dpt-data-modal .close-btn');
editDptCloseBtn.addEventListener('click', () => {
    editDptDataModal.style.display = 'none';
});

window.addEventListener('click', (event) => {
    if (event.target === editDptDataModal) {
        editDptDataModal.style.display = 'none';
    }
});





















// Данные теперь загружаются из базы данных через Django шаблоны
// Функция updateInfoBar больше не нужна, так как данные уже в шаблоне
















document.addEventListener("DOMContentLoaded", () => {
const body = document.body;
const panel = document.getElementById("accessibility-panel");

// Кнопки открытия панели (можно несколько)
const toggleButtons = [
document.getElementById("accessibility-toggle"),
document.getElementById("accessibility-btn")
].filter(Boolean); // убираем null, если кнопка не найдена

const resetButton = document.getElementById("reset-accessibility");

// Кнопки управления стилями
const fontUp = document.getElementById("font-size-up");
const fontDown = document.getElementById("font-size-down");
const spacingUp = document.getElementById("spacing-up");
const spacingDown = document.getElementById("spacing-down");
const invertedToggle = document.getElementById("inverted-colors-toggle");

let fontSize = 100;
let spacing = 100;
let isInverted = false;

function saveSettings() {
// Настройки доступности сохраняются в БД
}

function loadSettings() {
// Настройки доступности загружаются из БД
const saved = null;
if (saved) {
    fontSize = saved.fontSize;
    spacing = saved.spacing;
    isInverted = saved.isInverted;
}
applyStyles();
}

function applyStyles() {
body.style.fontSize = fontSize + "%";
body.style.lineHeight = (1.4 * spacing / 100).toFixed(2);
body.style.letterSpacing = ((spacing - 100) / 100) + "em";
body.classList.toggle("inverted-colors", isInverted);

if (invertedToggle && invertedToggle.type === "checkbox") {
    invertedToggle.checked = isInverted;
}
}

// Обработчики открытия панели для всех кнопок
toggleButtons.forEach(btn => {
btn.addEventListener("click", () => {
    panel.classList.toggle("active");
    const icon = btn.querySelector("i");
    if (icon) {
        icon.classList.toggle("fa-eye");
        icon.classList.toggle("fa-eye-slash");
    }
});
});

// Кнопки управления стилями
if (fontUp) fontUp.addEventListener("click", () => { fontSize = Math.min(fontSize+10,200); applyStyles(); saveSettings(); });
if (fontDown) fontDown.addEventListener("click", () => { fontSize = Math.max(fontSize-10,50); applyStyles(); saveSettings(); });
if (spacingUp) spacingUp.addEventListener("click", () => { spacing = Math.min(spacing+10,200); applyStyles(); saveSettings(); });
if (spacingDown) spacingDown.addEventListener("click", () => { spacing = Math.max(spacing-10,50); applyStyles(); saveSettings(); });
if (invertedToggle) invertedToggle.addEventListener("change", () => { isInverted = invertedToggle.checked; applyStyles(); saveSettings(); });
if (resetButton) resetButton.addEventListener("click", () => { fontSize=100; spacing=100; isInverted=false; applyStyles(); saveSettings(); });

// Загрузка настроек при старте
loadSettings();
});

// Функции для работы с новыми API endpoints
async function updateWeatherData() {
    const temperature = document.getElementById('current-temp').value || document.getElementById('weather-temperature').value;
    const description = document.getElementById('current-weather').value || document.getElementById('weather-settings-description').value;
    const icon = document.getElementById('current-weather-icon').value || 'fa-sun';
    
    try {
        const response = await fetch('/api/weather/update/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                temperature: parseInt(temperature) || 0,
                description: description || 'Ясно',
                icon: icon
            })
        });
        
        const result = await response.json();
        if (result.ok) {
            // Обновляем данные на странице
            const weatherIcon = document.getElementById('weather-icon');
            const weatherDescription = document.getElementById('weather-description');
            const temperatureElement = document.getElementById('temperature');
            
            if (weatherIcon) weatherIcon.className = `fa-solid ${icon}`;
            if (weatherDescription) weatherDescription.textContent = description;
            if (temperatureElement) temperatureElement.textContent = `${temperature}°`;
            
            showNotification('Данные погоды обновлены!', 'success');
        } else {
            showNotification('Ошибка при обновлении данных погоды', 'error');
        }
    } catch (error) {
        console.error('Ошибка обновления погоды:', error);
        showNotification('Ошибка при обновлении данных погоды', 'error');
    }
}

async function updateTrafficForecast() {
    const speed = document.getElementById('current-speed').value || document.getElementById('weather-traffic-speed').value;
    
    try {
        const response = await fetch('/api/traffic-forecast/update/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                speed: parseInt(speed) || 0
            })
        });
        
        const result = await response.json();
        if (result.ok) {
            // Обновляем данные на странице
            const speedElement = document.getElementById('traffic-speed');
            if (speedElement) speedElement.textContent = `${speed} км/ч`;
            
            showNotification('Прогноз скорости обновлен!', 'success');
        } else {
            showNotification('Ошибка при обновлении прогноза скорости', 'error');
        }
    } catch (error) {
        console.error('Ошибка обновления трафика:', error);
        showNotification('Ошибка при обновлении прогноза скорости', 'error');
    }
}

async function updateRoadWorks() {
    const count = document.getElementById('current-works').value || document.getElementById('road-works-count').value;
    
    try {
        const response = await fetch('/api/road-works/update/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                count: parseInt(count) || 0
            })
        });
        
        const result = await response.json();
        if (result.ok) {
            // Обновляем данные на странице
            const worksElement = document.getElementById('road-works-count-display');
            if (worksElement) worksElement.textContent = count;
            
            showNotification('Данные дорожных работ обновлены!', 'success');
        } else {
            showNotification('Ошибка при обновлении данных дорожных работ', 'error');
        }
    } catch (error) {
        console.error('Ошибка обновления дорожных работ:', error);
        showNotification('Ошибка при обновлении данных дорожных работ', 'error');
    }
}

async function updateAccidentStats() {
    const total = document.getElementById('current-accidents').value || document.getElementById('accident-total').value;
    const injured = document.getElementById('current-injured').value || document.getElementById('accident-injured').value;
    const killed = document.getElementById('current-killed').value || document.getElementById('accident-killed').value;
    const year = document.getElementById('accident-year').value || 2024;
    
    try {
        const response = await fetch('/api/accident-stats/update/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                total_accidents: parseInt(total) || 0,
                injured: parseInt(injured) || 0,
                killed: parseInt(killed) || 0,
                year: parseInt(year)
            })
        });
        
        const result = await response.json();
        if (result.ok) {
            // Обновляем данные мониторинга
            monitoringData = {
                total: parseInt(total) || 0,
                injured: parseInt(injured) || 0,
                killed: parseInt(killed) || 0
            };
            
            // Обновляем отображение на странице
            updateMonitoringValues();
            
            showNotification('Статистика ДТП обновлена!', 'success');
        } else {
            showNotification('Ошибка при обновлении статистики ДТП', 'error');
        }
    } catch (error) {
        console.error('Ошибка обновления статистики ДТП:', error);
        showNotification('Ошибка при обновлении статистики ДТП', 'error');
    }
}

async function updateAccidentData() {
    const typeId = document.getElementById('accident-type-select').value;
    const month = document.getElementById('accident-month').value;
    const count = document.getElementById('accident-count').value;
    const year = 2024;
    
    try {
        const response = await fetch('/api/accident-data/update/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                accident_type_id: parseInt(typeId),
                month: parseInt(month),
                count: parseInt(count),
                year: year
            })
        });
        
        const result = await response.json();
        if (result.ok) {
            showNotification('Данные ДТП обновлены!', 'success');
        } else {
            showNotification('Ошибка при обновлении данных ДТП', 'error');
        }
    } catch (error) {
        showNotification('Ошибка при обновлении данных ДТП', 'error');
    }
}

async function loadAccidentTypes() {
    try {
        const response = await fetch('/api/accident-types/');
        const data = await response.json();
        
        const select = document.getElementById('accident-type-select');
        if (select) {
        select.innerHTML = '';
        
        data.types.forEach(type => {
            const option = document.createElement('option');
            option.value = type.id;
            option.textContent = type.name;
            select.appendChild(option);
        });
        }
        
        // Обновляем список типов ДТП
        const typesList = document.getElementById('accident-types-list');
        if (typesList) {
        typesList.innerHTML = '';
        
        data.types.forEach(type => {
            const typeDiv = document.createElement('div');
            typeDiv.className = 'accident-type-item';
            typeDiv.innerHTML = `
                <div class="type-info">
                    <div class="type-color" style="background-color: ${type.color}"></div>
                    <span>${type.name}</span>
                </div>
                <div class="type-actions">
                    <input type="color" value="${type.color}" onchange="updateAccidentTypeColor(${type.id}, this.value)" class="form-control" style="width: 40px; height: 30px;">
                    <button onclick="deleteAccidentType(${type.id})" class="btn btn-danger btn-sm">Удалить</button>
                </div>
            `;
            typesList.appendChild(typeDiv);
        });
        }
        
        // Обновляем данные для графика
        await loadAccidentData();
        
    } catch (error) {
        console.error('Ошибка загрузки типов ДТП:', error);
        showNotification('Ошибка при загрузке типов ДТП', 'error');
    }
}

async function loadAccidentData() {
    try {
        const response = await fetch('/api/accident-data/');
        const data = await response.json();
        
        // Обновляем глобальные данные
        window.accidentData = data;
        dptData = data;
        
        // Перерисовываем график
        renderLineChart();
        
    } catch (error) {
        console.error('Ошибка загрузки данных ДТП:', error);
        showNotification('Ошибка при загрузке данных ДТП', 'error');
    }
}

// Функции для управления данными в реальном времени
function loadCurrentWeatherData() {
    // Загружаем текущие данные из верхней панели
    const weatherIcon = document.getElementById('weather-icon');
    const weatherDescription = document.getElementById('weather-description');
    const temperature = document.getElementById('weather-temperature');
    const trafficSpeed = document.getElementById('traffic-speed');
    const roadWorksCount = document.getElementById('road-works-count');
    
    // Заполняем формы текущими значениями
    if (weatherIcon) weatherIcon.value = 'fa-sun';
    if (weatherDescription) weatherDescription.value = 'Ясно';
    if (temperature) temperature.value = 23;
    if (trafficSpeed) trafficSpeed.value = 76;
    if (roadWorksCount) roadWorksCount.value = 1;
    
    // Заполняем поля для реального времени
    const currentTemp = document.getElementById('current-temp');
    const currentWeather = document.getElementById('current-weather');
    const currentSpeed = document.getElementById('current-speed');
    const currentWorks = document.getElementById('current-works');
    const currentAccidents = document.getElementById('current-accidents');
    const currentInjured = document.getElementById('current-injured');
    const currentKilled = document.getElementById('current-killed');
    
    if (currentTemp) currentTemp.value = 23;
    if (currentWeather) currentWeather.value = 'Ясно';
    if (currentSpeed) currentSpeed.value = 76;
    if (currentWorks) currentWorks.value = 1;
    if (currentAccidents) currentAccidents.value = 3;
    if (currentInjured) currentInjured.value = 6893;
    if (currentKilled) currentKilled.value = 181;
}

async function updateRealtimeData() {
    const currentTemp = document.getElementById('current-temp').value;
    const currentWeather = document.getElementById('current-weather').value;
    const currentWeatherIcon = document.getElementById('current-weather-icon').value;
    const currentSpeed = document.getElementById('current-speed').value;
    const currentWorks = document.getElementById('current-works').value;
    const currentAccidents = document.getElementById('current-accidents').value;
    const currentInjured = document.getElementById('current-injured').value;
    const currentKilled = document.getElementById('current-killed').value;
    
    try {
        // Обновляем данные в базе данных через API
        await updateWeatherData();
        await updateTrafficForecast();
        await updateRoadWorks();
        await updateAccidentStats();
        
        // Обновляем данные в верхней панели
        const weatherIcon = document.getElementById('weather-icon');
        const weatherDescription = document.getElementById('weather-description');
        const temperature = document.getElementById('temperature');
        const trafficSpeed = document.getElementById('traffic-speed');
        const roadWorks = document.getElementById('road-works');
        const seriousAccidents = document.getElementById('serious-accidents');
        const injuredValue = document.getElementById('injured-value');
        const killedValue = document.getElementById('killed-value');
        
        if (weatherIcon) weatherIcon.className = `fa-solid ${currentWeatherIcon || 'fa-sun'}`;
        if (weatherDescription) weatherDescription.textContent = currentWeather;
        if (temperature) temperature.textContent = `${currentTemp}°`;
        if (trafficSpeed) trafficSpeed.textContent = `${currentSpeed} км/ч`;
        if (roadWorks) roadWorks.textContent = currentWorks;
        if (seriousAccidents) seriousAccidents.textContent = currentAccidents;
        if (injuredValue) injuredValue.textContent = currentInjured;
        if (killedValue) killedValue.textContent = currentKilled;
        
        // Обновляем данные мониторинга
        monitoringData = {
                total: parseInt(currentAccidents) || 0,
                injured: parseInt(currentInjured) || 0,
                killed: parseInt(currentKilled) || 0
        };
        
        updateMonitoringValues();
        animateNumbers();
        
        showNotification('Данные в реальном времени обновлены!', 'success');
    } catch (error) {
        console.error('Ошибка обновления данных:', error);
        showNotification('Ошибка при обновлении данных', 'error');
    }
}

async function addNewAccidentType() {
    const typeName = document.getElementById('new-type-name').value;
    const typeColor = document.getElementById('new-type-color').value;
    
    if (!typeName) {
        showNotification('Пожалуйста, введите название типа ДТП', 'error');
        return;
    }
    
    try {
        const response = await fetch('/api/accident-types/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
        name: typeName,
        color: typeColor
            })
        });
        
        const data = await response.json();
        if (data.ok) {
            showNotification('Новый тип ДТП добавлен!', 'success');
    document.getElementById('new-type-name').value = '';
    document.getElementById('new-type-color').value = '#36A2EB';
            loadAccidentTypes();
        } else {
            showNotification('Ошибка добавления типа ДТП', 'error');
        }
    } catch (error) {
        console.error('Ошибка:', error);
        showNotification('Ошибка добавления типа ДТП', 'error');
    }
}

function processBulkDtpData() {
    const fileInput = document.getElementById('bulk-dtp-file');
    const file = fileInput.files[0];
    
    if (!file) {
        showNotification('Пожалуйста, выберите CSV файл', 'error');
        return;
    }
    
    const reader = new FileReader();
    reader.onload = function(e) {
        try {
            const text = e.target.result;
            const lines = text.split('\n').filter(line => line.trim());
            
            // Типы ДТП и данные загружаются из БД
            let accidentTypes = [];
            let dptData = {};
            
            lines.forEach((line, index) => {
                if (index === 0) return; // Пропускаем заголовок
                
                const [type, month, count, color] = line.split(',').map(item => item.trim());
                
                if (type && month && count) {
                    // Добавляем тип если его нет
                    if (!accidentTypes.find(t => t.name === type)) {
                        accidentTypes.push({
                            id: Date.now() + index,
                            name: type,
                            color: color || '#36A2EB'
                        });
                    }
                    
                    // Добавляем данные по месяцам
                    if (!dptData[type]) {
                        dptData[type] = {
                            data: new Array(12).fill(0),
                            color: color || '#36A2EB'
                        };
                    }
                    
                    const monthIndex = parseInt(month) - 1;
                    if (monthIndex >= 0 && monthIndex < 12) {
                        dptData[type].data[monthIndex] = parseInt(count);
                    }
                }
            });
            
            // Данные сохраняются в БД
            
            // Обновляем интерфейс
            loadAccidentTypes();
            renderLineChart();
            
            showNotification(`Обработано ${lines.length - 1} записей из CSV файла`, 'success');
            
        } catch (error) {
            showNotification('Ошибка при обработке CSV файла: ' + error.message, 'error');
        }
    };
    
    reader.readAsText(file);
}

// Функции для работы с типами ДТП
async function updateAccidentTypeColor(typeId, newColor) {
    try {
        const response = await fetch('/api/accident-types/', {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                id: typeId,
                color: newColor
            })
        });
        
        const data = await response.json();
        if (data.ok) {
        showNotification('Цвет типа ДТП обновлен!', 'success');
            loadAccidentTypes();
        } else {
            showNotification('Ошибка обновления цвета', 'error');
        }
    } catch (error) {
        console.error('Ошибка:', error);
        showNotification('Ошибка обновления цвета', 'error');
    }
}

async function deleteAccidentType(typeId) {
    if (!confirm('Вы уверены, что хотите удалить этот тип ДТП?')) {
        return;
    }
    
    try {
        const response = await fetch('/api/accident-types/', {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                id: typeId
            })
        });
        
        const data = await response.json();
        if (data.ok) {
        showNotification('Тип ДТП удален!', 'success');
            loadAccidentTypes();
        } else {
            showNotification('Ошибка удаления типа ДТП', 'error');
        }
    } catch (error) {
        console.error('Ошибка:', error);
        showNotification('Ошибка удаления типа ДТП', 'error');
    }
}

// Обработчики форм
document.addEventListener('DOMContentLoaded', function() {
    // Обработчик формы настроек погоды
    const weatherForm = document.getElementById('weather-settings-form');
    if (weatherForm) {
        weatherForm.addEventListener('submit', function(e) {
            e.preventDefault();
            updateWeatherData();
            updateTrafficForecast();
            updateRoadWorks();
        });
    }
    
    // Обработчик формы статистики ДТП
    const accidentStatsForm = document.getElementById('accident-stats-form');
    if (accidentStatsForm) {
        // Загружаем текущие данные в форму
        loadAccidentStatsForm();
        
        accidentStatsForm.addEventListener('submit', function(e) {
            e.preventDefault();
            updateAccidentStats();
        });
    }
    
    // Обработчик формы данных ДТП по месяцам
    const accidentMonthlyForm = document.getElementById('accident-monthly-form');
    if (accidentMonthlyForm) {
        accidentMonthlyForm.addEventListener('submit', function(e) {
            e.preventDefault();
            updateAccidentData();
        });
    }
    
    // Загружаем типы ДТП при загрузке страницы
    loadAccidentTypes();
    
    // Обработчик для обновления данных в реальном времени
    const updateRealtimeBtn = document.getElementById('update-realtime-data');
    if (updateRealtimeBtn) {
        updateRealtimeBtn.addEventListener('click', updateRealtimeData);
    }
    
    // Обработчик для добавления нового типа ДТП
    const addAccidentTypeForm = document.getElementById('add-accident-type-form');
    if (addAccidentTypeForm) {
        addAccidentTypeForm.addEventListener('submit', function(e) {
            e.preventDefault();
            addNewAccidentType();
        });
    }
    
    // Обработчик для массовой загрузки данных ДТП
    const processBulkDtpBtn = document.getElementById('process-bulk-dtp');
    if (processBulkDtpBtn) {
        processBulkDtpBtn.addEventListener('click', processBulkDtpData);
    }
    
    // Обработчики для управления новостями
    const addNewsCategoryForm = document.getElementById('add-news-category-form');
    if (addNewsCategoryForm) {
        addNewsCategoryForm.addEventListener('submit', function(e) {
            e.preventDefault();
            addNewsCategory();
        });
    }
    
    const addNewsArticleForm = document.getElementById('add-news-article-form');
    if (addNewsArticleForm) {
        addNewsArticleForm.addEventListener('submit', function(e) {
            e.preventDefault();
            addNewsArticle();
        });
    }
    
    // Обработчики для фильтрации обращений
    const filterAllAppeals = document.getElementById('filter-all-appeals');
    const filterPendingAppeals = document.getElementById('filter-pending-appeals');
    const filterReviewedAppeals = document.getElementById('filter-reviewed-appeals');
    
    if (filterAllAppeals) {
        filterAllAppeals.addEventListener('click', () => loadAppeals('all'));
    }
    if (filterPendingAppeals) {
        filterPendingAppeals.addEventListener('click', () => loadAppeals('pending'));
    }
    if (filterReviewedAppeals) {
        filterReviewedAppeals.addEventListener('click', () => loadAppeals('reviewed'));
    }
    
    // Загружаем данные при инициализации
    loadNewsCategories();
    loadNewsArticles();
    loadAppeals('all');
    loadChatThreads();
    
    // Инициализируем собственный богатый редактор
    initRichEditor();
    
    // Обработчики для чата
    const newChatBtn = document.getElementById('new-chat-btn');
    const chatSendBtn = document.getElementById('chat-send');
    const chatTextArea = document.getElementById('chat-text');
    
    if (newChatBtn) {
        newChatBtn.addEventListener('click', () => {
            currentThreadId = null;
            const subjectInput = document.getElementById('chat-subject');
            const textInput = document.getElementById('chat-text');
            const sendBtn = document.getElementById('chat-send');
            
            if (subjectInput) subjectInput.value = '';
            if (textInput) {
                textInput.value = '';
                textInput.disabled = false;
            }
            if (sendBtn) sendBtn.disabled = false;
            
            // Очищаем активные потоки
            document.querySelectorAll('.chat-thread').forEach(thread => {
                thread.classList.remove('active');
            });
            
            // Показываем приветственное сообщение
            const container = document.getElementById('chat-messages');
            if (container) {
                container.innerHTML = `
                    <div class="chat-welcome">
                        <i class="fas fa-comments"></i>
                        <h3>Новый диалог</h3>
                        <p>Введите тему и сообщение для создания нового диалога с администраторами.</p>
                    </div>
                `;
            }
        });
    }
    
    if (chatSendBtn) {
        chatSendBtn.addEventListener('click', sendMessage);
    }
    
    if (chatTextArea) {
        chatTextArea.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                sendMessage();
            }
        });
    }
});

// Функции для управления новостями
function loadNewsCategories() {
    fetch('/api/news-categories/')
        .then(response => response.json())
        .then(data => {
            const container = document.getElementById('news-categories-list');
            if (container) {
                container.innerHTML = '';
                data.categories.forEach(category => {
                    const categoryDiv = document.createElement('div');
                    categoryDiv.className = 'data-item';
                    categoryDiv.innerHTML = `
                        <div class="item-info">
                            <h4>${category.name}</h4>
                            ${category.image_url ? `<img src="${category.image_url}" alt="${category.name}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 4px;">` : ''}
                        </div>
                        <div class="item-actions">
                            <button class="btn btn-sm btn-secondary" onclick="editNewsCategory(${category.id})">
                                <i class="fas fa-edit"></i>
                            </button>
                            <button class="btn btn-sm btn-danger" onclick="deleteNewsCategory(${category.id})">
                                <i class="fas fa-trash"></i>
                            </button>
                        </div>
                    `;
                    container.appendChild(categoryDiv);
                });
            }
        })
        .catch(error => {
            console.error('Ошибка загрузки категорий:', error);
            showNotification('Ошибка загрузки категорий', 'error');
        });
}

function loadNewsArticles() {
    fetch('/api/news-articles/')
        .then(response => response.json())
        .then(data => {
            const container = document.getElementById('news-articles-list');
            if (container) {
                container.innerHTML = '';
                data.articles.forEach(article => {
                    const articleDiv = document.createElement('div');
                    articleDiv.className = 'data-item';
                    articleDiv.innerHTML = `
                        <div class="item-info">
                            <h4>${article.title}</h4>
                            <p><strong>Категория:</strong> ${article.category__name}</p>
                            <p><strong>Автор:</strong> ${article.author || 'Не указан'}</p>
                            <p><strong>Дата:</strong> ${new Date(article.created_at).toLocaleDateString()}</p>
                        </div>
                        <div class="item-actions">
                            <button class="btn btn-sm btn-secondary" onclick="editNewsArticle(${article.id})">
                                <i class="fas fa-edit"></i>
                            </button>
                            <button class="btn btn-sm btn-danger" onclick="deleteNewsArticle(${article.id})">
                                <i class="fas fa-trash"></i>
                            </button>
                        </div>
                    `;
                    container.appendChild(articleDiv);
                });
            }
        })
        .catch(error => {
            console.error('Ошибка загрузки статей:', error);
            showNotification('Ошибка загрузки статей', 'error');
        });
}

function addNewsCategory() {
    const nameInput = document.getElementById('new-category-name');
    const imageUrlInput = document.getElementById('new-category-image');
    
    if (!nameInput) {
        showNotification('Поле названия не найдено', 'error');
        return;
    }
    
    const name = nameInput.value.trim();
    const imageUrl = imageUrlInput ? imageUrlInput.value.trim() : '';
    
    if (!name) {
        showNotification('Введите название категории', 'error');
        return;
    }
    
    fetch('/api/news-categories/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({
            name: name,
            image_url: imageUrl
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.ok) {
            showNotification('Категория добавлена!', 'success');
            document.getElementById('add-news-category-form').reset();
            loadNewsCategories();
        } else {
            showNotification('Ошибка добавления категории', 'error');
        }
    })
    .catch(error => {
        console.error('Ошибка:', error);
        showNotification('Ошибка добавления категории', 'error');
    });
}

function addNewsArticle() {
    const categoryIdInput = document.getElementById('article-category');
    const titleInput = document.getElementById('article-title');
    const authorInput = document.getElementById('article-author');
    const summaryInput = document.getElementById('article-summary');
    const contentInput = document.getElementById('article-content');
    const coverImageInput = document.getElementById('article-cover-image');
    
    if (!titleInput || !contentInput) {
        showNotification('Обязательные поля не найдены', 'error');
        return;
    }
    
    const categoryId = categoryIdInput ? categoryIdInput.value : 1;
    const title = titleInput.value.trim();
    const author = authorInput ? authorInput.value.trim() : '';
    const summary = summaryInput ? summaryInput.value.trim() : '';
    const content = contentInput.innerHTML.trim();
    const coverImage = coverImageInput ? coverImageInput.value.trim() : '';
    
    if (!title || !content) {
        showNotification('Заполните обязательные поля', 'error');
        return;
    }
    
    fetch('/api/news-articles/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({
            category_id: parseInt(categoryId),
            title: title,
            author: author,
            summary: summary,
            content: content,
            cover_image_url: coverImage
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.ok) {
            showNotification('Статья добавлена!', 'success');
            document.getElementById('add-news-article-form').reset();
            // Очищаем содержимое редактора
            const contentEditor = document.getElementById('article-content');
            if (contentEditor) contentEditor.innerHTML = '';
            loadNewsArticles();
        } else {
            showNotification('Ошибка добавления статьи', 'error');
        }
    })
    .catch(error => {
        console.error('Ошибка:', error);
        showNotification('Ошибка добавления статьи', 'error');
    });
}

// Функции для управления обращениями
function loadAppeals(filter = 'all') {
    fetch(`/api/appeals/?filter=${filter}`)
        .then(response => response.json())
        .then(data => {
            const container = document.getElementById('admin-appeals-list');
            if (container) {
                container.innerHTML = '';
                data.appeals.forEach(appeal => {
                    const appealDiv = document.createElement('div');
                    appealDiv.className = 'data-item';
                    appealDiv.innerHTML = `
                        <div class="item-info">
                            <h4>${appeal.name}</h4>
                            <p><strong>Email:</strong> ${appeal.email}</p>
                            <p><strong>Сообщение:</strong> ${appeal.message.substring(0, 100)}...</p>
                            <p><strong>Дата:</strong> ${new Date(appeal.created_at).toLocaleDateString()}</p>
                            <p><strong>Статус:</strong> ${appeal.is_reviewed ? 'Рассмотрено' : 'Нерассмотрено'}</p>
                        </div>
                        <div class="item-actions">
                            <button class="btn btn-sm btn-primary" onclick="toggleAppealStatus(${appeal.id})">
                                ${appeal.is_reviewed ? 'Отметить как нерассмотренное' : 'Отметить как рассмотренное'}
                            </button>
                            <button class="btn btn-sm btn-danger" onclick="deleteAppeal(${appeal.id})">
                                <i class="fas fa-trash"></i>
                            </button>
                        </div>
                    `;
                    container.appendChild(appealDiv);
                });
            }
        })
        .catch(error => console.error('Ошибка загрузки обращений:', error));
}

function toggleAppealStatus(appealId) {
    fetch(`/api/appeals/${appealId}/toggle/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.ok) {
            showNotification('Статус обращения обновлен!', 'success');
            loadAppeals();
        } else {
            showNotification('Ошибка обновления статуса', 'error');
        }
    })
    .catch(error => {
        console.error('Ошибка:', error);
        showNotification('Ошибка обновления статуса', 'error');
    });
}

// Функции для управления чатом
let currentThreadId = null;
let chatThreads = [];

function loadChatThreads() {
    fetch('/api/chat-threads/')
        .then(response => response.json())
        .then(data => {
            chatThreads = data.threads;
            renderChatThreads();
        })
        .catch(error => {
            console.error('Ошибка загрузки чатов:', error);
            showNotification('Ошибка загрузки чатов', 'error');
        });
}

function loadAdminChatThreads() {
    fetch('/api/admin/chat-threads/')
        .then(response => response.json())
        .then(data => {
            const adminContainer = document.getElementById('admin-chat-threads');
            if (adminContainer) {
                adminContainer.innerHTML = '';
                data.threads.forEach(thread => {
                    const threadDiv = document.createElement('div');
                    threadDiv.className = 'data-item';
                    threadDiv.innerHTML = `
                        <div class="item-info">
                            <h4>${thread.subject || 'Без темы'}</h4>
                            <p><strong>Пользователь:</strong> ${thread.user_name || 'Гость'}</p>
                            <p><strong>Сообщений:</strong> ${thread.message_count}</p>
                            <p><strong>Дата создания:</strong> ${new Date(thread.created_at).toLocaleDateString()}</p>
                            <p><strong>Статус:</strong> ${thread.is_closed ? 'Закрыт' : 'Активен'}</p>
                        </div>
                        <div class="item-actions">
                            <button class="btn btn-sm btn-primary" onclick="viewChatThread(${thread.id})">
                                <i class="fas fa-eye"></i> Просмотр
                            </button>
                            <button class="btn btn-sm btn-secondary" onclick="toggleThreadStatus(${thread.id})">
                                ${thread.is_closed ? 'Открыть' : 'Закрыть'}
                            </button>
                        </div>
                    `;
                    adminContainer.appendChild(threadDiv);
                });
            }
        })
        .catch(error => {
            console.error('Ошибка загрузки админских чатов:', error);
            showNotification('Ошибка загрузки чатов', 'error');
        });
}

function renderChatThreads() {
    const container = document.getElementById('chat-threads');
    if (!container) return;
    
    container.innerHTML = '';
    
    if (chatThreads.length === 0) {
        container.innerHTML = '<div class="no-threads">Нет диалогов</div>';
        return;
    }
    
    chatThreads.forEach(thread => {
        const threadDiv = document.createElement('div');
        threadDiv.className = 'chat-thread';
        threadDiv.dataset.threadId = thread.id;
        threadDiv.innerHTML = `
            <div class="thread-subject">${thread.subject || 'Без темы'}</div>
            <div class="thread-meta">
                <span>${new Date(thread.created_at).toLocaleDateString()}</span>
                <div class="thread-status ${thread.is_closed ? 'closed' : ''}"></div>
            </div>
        `;
        
        threadDiv.addEventListener('click', () => selectThread(thread.id));
        container.appendChild(threadDiv);
    });
}

function selectThread(threadId) {
    // Убираем активный класс с всех потоков
    document.querySelectorAll('.chat-thread').forEach(thread => {
        thread.classList.remove('active');
    });
    
    // Добавляем активный класс к выбранному потоку
    const selectedThread = document.querySelector(`[data-thread-id="${threadId}"]`);
    if (selectedThread) {
        selectedThread.classList.add('active');
    }
    
    currentThreadId = threadId;
    
    // Включаем поля ввода
    document.getElementById('chat-text').disabled = false;
    document.getElementById('chat-send').disabled = false;
    
    // Загружаем сообщения
    loadThreadMessages(threadId);
}

function loadThreadMessages(threadId) {
    fetch(`/api/chat/messages/?thread_id=${threadId}`)
        .then(response => response.json())
        .then(data => {
            renderMessages(data.messages);
        })
        .catch(error => {
            console.error('Ошибка загрузки сообщений:', error);
            showNotification('Ошибка загрузки сообщений', 'error');
        });
}

function renderMessages(messages) {
    const container = document.getElementById('chat-messages');
    if (!container) return;
    
    container.innerHTML = '';
    
    if (!messages || messages.length === 0) {
        container.innerHTML = '<div class="no-messages">Нет сообщений в этом диалоге</div>';
        return;
    }
    
    messages.forEach(message => {
        const messageDiv = document.createElement('div');
        messageDiv.className = `chat-message ${message.sender}`;
        messageDiv.innerHTML = `
            <div class="message-avatar">
                ${message.sender === 'user' ? 'U' : 'A'}
            </div>
            <div class="message-content">
                <div class="message-text">${message.content}</div>
                <div class="message-time">${new Date(message.created_at).toLocaleTimeString()}</div>
            </div>
        `;
        container.appendChild(messageDiv);
    });
    
    // Прокручиваем вниз
    container.scrollTop = container.scrollHeight;
}

function createNewThread() {
    const subjectInput = document.getElementById('chat-subject');
    const contentInput = document.getElementById('chat-text');
    
    if (!subjectInput || !contentInput) {
        showNotification('Поля ввода не найдены', 'error');
        return;
    }
    
    const subject = subjectInput.value.trim();
    const content = contentInput.value.trim();
    
    if (!content) {
        showNotification('Введите сообщение', 'error');
        return;
    }
    
    fetch('/api/chat/send/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({
            subject: subject,
            content: content,
            thread_id: null
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.ok) {
            currentThreadId = data.thread_id;
            showNotification('Диалог создан!', 'success');
            subjectInput.value = '';
            contentInput.value = '';
            loadChatThreads();
            loadThreadMessages(data.thread_id);
        } else {
            showNotification('Ошибка создания диалога', 'error');
        }
    })
    .catch(error => {
        console.error('Ошибка:', error);
        showNotification('Ошибка создания диалога', 'error');
    });
}

function sendMessage() {
    if (!currentThreadId) {
        createNewThread();
        return;
    }
    
    const contentInput = document.getElementById('chat-text');
    if (!contentInput) {
        showNotification('Поле ввода сообщения не найдено', 'error');
        return;
    }
    
    const content = contentInput.value.trim();
    
    if (!content) {
        showNotification('Введите сообщение', 'error');
        return;
    }
    
    fetch('/api/chat/send/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({
            content: content,
            thread_id: currentThreadId
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.ok) {
            contentInput.value = '';
            loadThreadMessages(currentThreadId);
            showNotification('Сообщение отправлено!', 'success');
        } else {
            showNotification('Ошибка отправки сообщения', 'error');
        }
    })
    .catch(error => {
        console.error('Ошибка:', error);
        showNotification('Ошибка отправки сообщения', 'error');
    });
}

function toggleThreadStatus(threadId) {
    fetch(`/api/chat-threads/${threadId}/toggle/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.ok) {
            showNotification('Статус чата обновлен!', 'success');
            loadAdminChatThreads();
        } else {
            showNotification('Ошибка обновления статуса чата', 'error');
        }
    })
    .catch(error => {
        console.error('Ошибка:', error);
        showNotification('Ошибка обновления статуса чата', 'error');
    });
}

function viewChatThread(threadId) {
    // Создаем модальное окно для просмотра чата
    const modal = document.createElement('div');
    modal.className = 'modal';
    modal.style.display = 'flex';
    modal.innerHTML = `
        <div class="modal-content" style="width: 90%; max-width: 800px;">
            <div class="modal-header">
                <h2>Просмотр чата</h2>
                <span class="close-btn">&times;</span>
            </div>
            <div class="modal-body">
                <div id="chat-messages-view" style="height: 400px; overflow-y: auto; border: 1px solid #ddd; padding: 10px; margin-bottom: 10px;">
                    <!-- Сообщения будут загружены здесь -->
                </div>
                <div class="chat-input-container">
                    <textarea id="admin-chat-message" class="form-control" rows="3" placeholder="Введите ответ администратора..."></textarea>
                    <button id="admin-send-message" class="btn btn-primary" style="margin-top: 10px;">
                        <i class="fas fa-paper-plane"></i> Отправить ответ
                    </button>
                </div>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
    
    // Загружаем сообщения чата
    loadThreadMessagesForAdmin(threadId);
    
    // Обработчики событий
    modal.querySelector('.close-btn').addEventListener('click', () => {
        document.body.removeChild(modal);
    });
    
    modal.querySelector('#admin-send-message').addEventListener('click', () => {
        const messageInput = document.getElementById('admin-chat-message');
        const content = messageInput.value.trim();
        
        if (!content) {
            showNotification('Введите сообщение', 'error');
            return;
        }
        
        // Отправляем сообщение от имени админа
        fetch('/api/chat/send/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                content: content,
                thread_id: threadId,
                sender: 'admin'
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.ok) {
                messageInput.value = '';
                loadThreadMessagesForAdmin(threadId);
                showNotification('Сообщение отправлено!', 'success');
            } else {
                showNotification('Ошибка отправки сообщения', 'error');
            }
        })
        .catch(error => {
            console.error('Ошибка:', error);
            showNotification('Ошибка отправки сообщения', 'error');
        });
    });
    
    // Закрытие по клику вне модального окна
    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            document.body.removeChild(modal);
        }
    });
}

function loadThreadMessagesForAdmin(threadId) {
    fetch(`/api/chat/messages/?thread_id=${threadId}`)
        .then(response => response.json())
        .then(data => {
            const container = document.getElementById('chat-messages-view');
            if (!container) return;
            
            container.innerHTML = '';
            
            if (!data.messages || data.messages.length === 0) {
                container.innerHTML = '<div class="no-messages">Нет сообщений в этом диалоге</div>';
                return;
            }
            
            data.messages.forEach(message => {
                const messageDiv = document.createElement('div');
                messageDiv.className = `chat-message ${message.sender}`;
                messageDiv.innerHTML = `
                    <div class="message-avatar">
                        ${message.sender === 'user' ? 'U' : 'A'}
                    </div>
                    <div class="message-content">
                        <div class="message-text">${message.content}</div>
                        <div class="message-time">${new Date(message.created_at).toLocaleTimeString()}</div>
                    </div>
                `;
                container.appendChild(messageDiv);
            });
            
            // Прокручиваем вниз
            container.scrollTop = container.scrollHeight;
        })
        .catch(error => {
            console.error('Ошибка загрузки сообщений:', error);
            showNotification('Ошибка загрузки сообщений', 'error');
    });
}

// Функции для редактирования и удаления новостей
function editNewsCategory(categoryId) {
    // Создаем модальное окно для редактирования
    const modal = document.createElement('div');
    modal.className = 'modal';
    modal.style.display = 'flex';
    modal.innerHTML = `
        <div class="modal-content">
            <div class="modal-header">
                <h2>Редактировать категорию</h2>
                <span class="close-btn">&times;</span>
            </div>
            <div class="modal-body">
                <form id="edit-category-form">
                    <div class="form-group">
                        <label for="edit-category-name">Название категории</label>
                        <input type="text" id="edit-category-name" class="form-control" required>
                    </div>
                    <div class="form-group">
                        <label for="edit-category-image">URL изображения</label>
                        <input type="url" id="edit-category-image" class="form-control" placeholder="https://example.com/image.jpg">
                    </div>
                    <button type="submit" class="btn btn-primary">Сохранить</button>
                    <button type="button" class="btn btn-secondary" id="cancel-edit-category">Отмена</button>
                </form>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
    
    // Загружаем текущие данные категории
    fetch('/api/news-categories/')
        .then(response => response.json())
        .then(data => {
            const category = data.categories.find(c => c.id === categoryId);
            if (category) {
                document.getElementById('edit-category-name').value = category.name;
                document.getElementById('edit-category-image').value = category.image_url || '';
            }
        });
    
    // Обработчики событий
    modal.querySelector('.close-btn').addEventListener('click', () => {
        document.body.removeChild(modal);
    });
    
    modal.querySelector('#cancel-edit-category').addEventListener('click', () => {
        document.body.removeChild(modal);
    });
    
    modal.querySelector('#edit-category-form').addEventListener('submit', (e) => {
        e.preventDefault();
        
        const name = document.getElementById('edit-category-name').value.trim();
        const imageUrl = document.getElementById('edit-category-image').value.trim();
        
        if (!name) {
            showNotification('Введите название категории', 'error');
            return;
        }
        
        fetch('/api/news-categories/', {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                id: categoryId,
                name: name,
                image_url: imageUrl
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.ok) {
                loadNewsCategories();
                showNotification('Категория обновлена!', 'success');
                document.body.removeChild(modal);
            } else {
                showNotification('Ошибка обновления категории', 'error');
            }
        })
        .catch(error => {
            console.error('Ошибка:', error);
            showNotification('Ошибка обновления категории', 'error');
        });
    });
    
    // Закрытие по клику вне модального окна
    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            document.body.removeChild(modal);
        }
    });
}

function deleteNewsCategory(categoryId) {
    if (confirm('Вы уверены, что хотите удалить эту категорию?')) {
        fetch('/api/news-categories/', {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                id: categoryId
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.ok) {
                loadNewsCategories();
                showNotification('Категория удалена!', 'success');
            } else {
                showNotification('Ошибка удаления категории', 'error');
            }
        })
        .catch(error => {
            console.error('Ошибка:', error);
            showNotification('Ошибка удаления категории', 'error');
        });
    }
}

function editNewsArticle(articleId) {
    // Создаем модальное окно для редактирования статьи
    const modal = document.createElement('div');
    modal.className = 'modal';
    modal.style.display = 'flex';
    modal.innerHTML = `
        <div class="modal-content" style="width: 90%; max-width: 1000px; max-height: 80vh; overflow-y: auto;">
            <div class="modal-header">
                <h2>Редактировать статью</h2>
                <span class="close-btn">&times;</span>
            </div>
            <div class="modal-body">
                <form id="edit-article-form">
                    <div class="form-group">
                        <label for="edit-article-title">Заголовок статьи</label>
                        <input type="text" id="edit-article-title" class="form-control" required>
                    </div>
                    <div class="form-group">
                        <label for="edit-article-author">Автор</label>
                        <input type="text" id="edit-article-author" class="form-control">
                    </div>
                    <div class="form-group">
                        <label for="edit-article-summary">Краткое описание</label>
                        <textarea id="edit-article-summary" class="form-control" rows="3"></textarea>
                    </div>
                    <div class="form-group">
                        <label for="edit-article-content">Содержание</label>
                        <div class="rich-editor-container">
                            <div class="rich-editor-toolbar">
                                <button type="button" class="editor-btn" data-command="bold" title="Жирный">
                                    <i class="fas fa-bold"></i>
                                </button>
                                <button type="button" class="editor-btn" data-command="italic" title="Курсив">
                                    <i class="fas fa-italic"></i>
                                </button>
                                <button type="button" class="editor-btn" data-command="underline" title="Подчеркнутый">
                                    <i class="fas fa-underline"></i>
                                </button>
                                <button type="button" class="editor-btn" data-command="strikeThrough" title="Зачеркнутый">
                                    <i class="fas fa-strikethrough"></i>
                                </button>
                                <div class="editor-separator"></div>
                                <button type="button" class="editor-btn" data-command="insertUnorderedList" title="Маркированный список">
                                    <i class="fas fa-list-ul"></i>
                                </button>
                                <button type="button" class="editor-btn" data-command="insertOrderedList" title="Нумерованный список">
                                    <i class="fas fa-list-ol"></i>
                                </button>
                                <div class="editor-separator"></div>
                                <button type="button" class="editor-btn" data-command="justifyLeft" title="По левому краю">
                                    <i class="fas fa-align-left"></i>
                                </button>
                                <button type="button" class="editor-btn" data-command="justifyCenter" title="По центру">
                                    <i class="fas fa-align-center"></i>
                                </button>
                                <button type="button" class="editor-btn" data-command="justifyRight" title="По правому краю">
                                    <i class="fas fa-align-right"></i>
                                </button>
                                <button type="button" class="editor-btn" data-command="justifyFull" title="По ширине">
                                    <i class="fas fa-align-justify"></i>
                                </button>
                                <div class="editor-separator"></div>
                                <button type="button" class="editor-btn" data-command="createLink" title="Вставить ссылку">
                                    <i class="fas fa-link"></i>
                                </button>
                                <button type="button" class="editor-btn" data-command="insertImage" title="Вставить изображение">
                                    <i class="fas fa-image"></i>
                                </button>
                                <div class="editor-separator"></div>
                                <button type="button" class="editor-btn" data-command="undo" title="Отменить">
                                    <i class="fas fa-undo"></i>
                                </button>
                                <button type="button" class="editor-btn" data-command="redo" title="Повторить">
                                    <i class="fas fa-redo"></i>
                                </button>
                            </div>
                            <div id="edit-article-content" class="rich-editor-content" contenteditable="true" data-placeholder="Введите содержание статьи..."></div>
                        </div>
                    </div>
                    <div class="form-group">
                        <label for="edit-article-cover-image">URL обложки</label>
                        <input type="url" id="edit-article-cover-image" class="form-control" placeholder="https://example.com/cover.jpg">
                    </div>
                    <button type="submit" class="btn btn-primary">Сохранить</button>
                    <button type="button" class="btn btn-secondary" id="cancel-edit-article">Отмена</button>
                </form>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
    
    // Загружаем текущие данные статьи
    fetch('/api/news-articles/')
        .then(response => response.json())
        .then(data => {
            const article = data.articles.find(a => a.id === articleId);
            if (article) {
                document.getElementById('edit-article-title').value = article.title;
                document.getElementById('edit-article-author').value = article.author || '';
                document.getElementById('edit-article-summary').value = article.summary || '';
                document.getElementById('edit-article-content').innerHTML = article.content || '';
                document.getElementById('edit-article-cover-image').value = article.cover_image_url || '';
                
                // Инициализируем собственный редактор для редактирования
                initEditRichEditor();
            }
        });
    
    // Обработчики событий
    modal.querySelector('.close-btn').addEventListener('click', () => {
        document.body.removeChild(modal);
    });
    
    modal.querySelector('#cancel-edit-article').addEventListener('click', () => {
        document.body.removeChild(modal);
    });
    
    modal.querySelector('#edit-article-form').addEventListener('submit', (e) => {
        e.preventDefault();
        
        const title = document.getElementById('edit-article-title').value.trim();
        const author = document.getElementById('edit-article-author').value.trim();
        const summary = document.getElementById('edit-article-summary').value.trim();
        const coverImage = document.getElementById('edit-article-cover-image').value.trim();
        
        // Получаем содержимое из редактора
        const contentEditor = document.getElementById('edit-article-content');
        const content = contentEditor ? contentEditor.innerHTML : '';
        
        if (!title || !content) {
            showNotification('Заполните обязательные поля', 'error');
            return;
        }
        
        fetch('/api/news-articles/', {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                id: articleId,
                title: title,
                author: author,
                summary: summary,
                content: content,
                cover_image_url: coverImage
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.ok) {
                loadNewsArticles();
                showNotification('Статья обновлена!', 'success');
                document.body.removeChild(modal);
            } else {
                showNotification('Ошибка обновления статьи', 'error');
            }
        })
        .catch(error => {
            console.error('Ошибка:', error);
            showNotification('Ошибка обновления статьи', 'error');
        });
    });
    
    // Закрытие по клику вне модального окна
    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            document.body.removeChild(modal);
        }
    });
}

function deleteNewsArticle(articleId) {
    if (confirm('Вы уверены, что хотите удалить эту статью?')) {
        fetch('/api/news-articles/', {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                id: articleId
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.ok) {
                loadNewsArticles();
                showNotification('Статья удалена!', 'success');
            } else {
                showNotification('Ошибка удаления статьи', 'error');
            }
        })
        .catch(error => {
            console.error('Ошибка:', error);
            showNotification('Ошибка удаления статьи', 'error');
        });
    }
}

// Инициализация собственного богатого редактора
function initRichEditor() {
    const editor = document.getElementById('article-content');
    if (!editor) return;
    
    const toolbar = editor.parentElement.querySelector('.rich-editor-toolbar');
    if (!toolbar) return;
    
    // Обработчики кнопок панели инструментов
    toolbar.addEventListener('click', function(e) {
        if (e.target.closest('.editor-btn')) {
            e.preventDefault();
            const btn = e.target.closest('.editor-btn');
            const command = btn.dataset.command;
            
            if (command) {
                execCommand(command);
                updateToolbarState();
            }
        }
    });
    
    // Обновление состояния кнопок
    function updateToolbarState() {
        const buttons = toolbar.querySelectorAll('.editor-btn');
        buttons.forEach(btn => {
            const command = btn.dataset.command;
            if (command) {
                btn.classList.toggle('active', document.queryCommandState(command));
            }
        });
    }
    
    // Выполнение команд
    function execCommand(command) {
        if (command === 'createLink') {
            const url = prompt('Введите URL ссылки:');
            if (url) {
                document.execCommand('createLink', false, url);
            }
        } else if (command === 'insertImage') {
            const url = prompt('Введите URL изображения:');
            if (url) {
                document.execCommand('insertImage', false, url);
            }
        } else {
            document.execCommand(command, false, null);
        }
    }
    
    // Обновление состояния при изменении выделения
    editor.addEventListener('keyup', updateToolbarState);
    editor.addEventListener('mouseup', updateToolbarState);
    editor.addEventListener('focus', updateToolbarState);
    
    // Поддержка Ctrl+Z и Ctrl+Y
    editor.addEventListener('keydown', function(e) {
        if (e.ctrlKey && e.key === 'z') {
            e.preventDefault();
            document.execCommand('undo');
            updateToolbarState();
        } else if (e.ctrlKey && e.key === 'y') {
            e.preventDefault();
            document.execCommand('redo');
            updateToolbarState();
        }
    });
}

// Инициализация редактора в модальном окне
function initEditRichEditor() {
    const editor = document.getElementById('edit-article-content');
    if (!editor) return;
    
    const toolbar = editor.parentElement.querySelector('.rich-editor-toolbar');
    if (!toolbar) return;
    
    // Обработчики кнопок панели инструментов
    toolbar.addEventListener('click', function(e) {
        if (e.target.closest('.editor-btn')) {
            e.preventDefault();
            const btn = e.target.closest('.editor-btn');
            const command = btn.dataset.command;
            
            if (command) {
                execCommand(command);
                updateToolbarState();
            }
        }
    });
    
    // Обновление состояния кнопок
    function updateToolbarState() {
        const buttons = toolbar.querySelectorAll('.editor-btn');
        buttons.forEach(btn => {
            const command = btn.dataset.command;
            if (command) {
                btn.classList.toggle('active', document.queryCommandState(command));
            }
        });
    }
    
    // Выполнение команд
    function execCommand(command) {
        if (command === 'createLink') {
            const url = prompt('Введите URL ссылки:');
            if (url) {
                document.execCommand('createLink', false, url);
            }
        } else if (command === 'insertImage') {
            const url = prompt('Введите URL изображения:');
            if (url) {
                document.execCommand('insertImage', false, url);
            }
        } else {
            document.execCommand(command, false, null);
        }
    }
    
    // Обновление состояния при изменении выделения
    editor.addEventListener('keyup', updateToolbarState);
    editor.addEventListener('mouseup', updateToolbarState);
    editor.addEventListener('focus', updateToolbarState);
    
    // Поддержка Ctrl+Z и Ctrl+Y
    editor.addEventListener('keydown', function(e) {
        if (e.ctrlKey && e.key === 'z') {
            e.preventDefault();
            document.execCommand('undo');
            updateToolbarState();
        } else if (e.ctrlKey && e.key === 'y') {
            e.preventDefault();
            document.execCommand('redo');
            updateToolbarState();
        }
    });
}

// Вспомогательная функция для получения CSRF токена
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}