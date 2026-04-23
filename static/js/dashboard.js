(function () {
  'use strict';

  let selectedCategory = null;

  const citySection    = document.getElementById('citySection');
  const citySelect     = document.getElementById('citySelect');
  const resultsSection = document.getElementById('resultsSection');
  const chartsContainer = document.getElementById('chartsContainer');
  const summaryContainer = document.getElementById('summaryContainer');
  const loadingSpinner = document.getElementById('loadingSpinner');
  const subtitle       = document.getElementById('dashboardSubtitle');

  const CATEGORY_LABELS = {
    temperature: 'Temperature Trends',
    rainfall:    'Rainfall Patterns',
    extreme:     'Extreme Weather',
  };

  // Category buton clicks

  document.querySelectorAll('.cat-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.cat-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');

      selectedCategory = btn.dataset.category;
      subtitle.textContent = `Category: ${CATEGORY_LABELS[selectedCategory]} — now select a city.`;

      // reset downstream UI
      citySelect.innerHTML = '<option value="">— Choose a city —</option>';
      hideResults();
      citySection.style.display = 'block';

      fetchCities();
    });
  });

  // City dropdown

  citySelect.addEventListener('change', () => {
    const city = citySelect.value;
    if (!city) {
      hideResults();
      return;
    }
    fetchChart(selectedCategory, city);
  });

  // API

  function fetchCities() {
    fetch('/api/cities', { credentials: 'same-origin' })
      .then(r => r.json())
      .then(data => {
        if (data.error) {
          showError(data.error);
          return;
        }
        data.cities.forEach(city => {
          const opt = document.createElement('option');
          opt.value = city;
          opt.textContent = city;
          citySelect.appendChild(opt);
        });
      })
      .catch(() => showError('Failed to load city list. Please try again.'));
  }

  function fetchChart(category, city) {
    showSpinner();
    const url = `/api/chart?category=${encodeURIComponent(category)}&city=${encodeURIComponent(city)}`;
    fetch(url, { credentials: 'same-origin' })
      .then(r => r.json())
      .then(data => {
        hideSpinner();
        if (data.error) {
          showError(data.error);
          return;
        }
        renderCharts(data.charts);
        renderSummary(data.summary);
        resultsSection.style.display = 'block';
      })
      .catch(() => {
        hideSpinner();
        showError('Failed to load chart data. Please try again.');
      });
  }

  // Rendering helpers

  function renderCharts(charts) {
    chartsContainer.innerHTML = '';
    charts.forEach(b64 => {
      const img = document.createElement('img');
      img.src = 'data:image/png;base64,' + b64;
      img.className = 'plot-img';
      img.alt = 'Weather chart';
      chartsContainer.appendChild(img);
    });
  }

  function renderSummary(text) {
    summaryContainer.textContent = text;
    summaryContainer.style.display = 'block';
  }

  function showError(msg) {
    chartsContainer.innerHTML = `<p class="empty-msg" style="color:#f87171;">${msg}</p>`;
    summaryContainer.style.display = 'none';
    resultsSection.style.display = 'block';
  }

  function showSpinner() {
    chartsContainer.innerHTML = '';
    summaryContainer.style.display = 'none';
    loadingSpinner.style.display = 'flex';
    resultsSection.style.display = 'block';
  }

  function hideSpinner() {
    loadingSpinner.style.display = 'none';
  }

  function hideResults() {
    resultsSection.style.display = 'none';
    chartsContainer.innerHTML = '';
    summaryContainer.style.display = 'none';
  }
}());
