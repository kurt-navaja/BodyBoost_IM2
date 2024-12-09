document.addEventListener('DOMContentLoaded', function() {
  const moodSlider = document.getElementById('moodSlider');
  const currentMood = document.querySelector('.current-mood');
  const moodFactorsContainer = document.querySelector('.mood-factors');

  const moodFactorMap = {
    'Poor': [
      'Stressed',
      'Anxious',
      'Hurt',
      'Frustrated',
      'Overwhelmed',
      'Disappointed',
      'Irritated'
    ],
    'Fair': [
      'Indifferent',
      'Uncertain',
      'Hesitant',
      'Uneasy',
      'Neutral',
      'Bored',
      'Tired'
    ],
    'Good': [
      'Content',
      'Hopeful',
      'Calm',
      'Satisfied',
      'Optimistic',
      'Steady',
      'Appreciative'
    ],
    'Great': [
      'Energized',
      'Happy',
      'Accomplished',
      'Confident',
      'Cheerful',
      'Encouraged'
    ],
    'Excellent': [
      'Triumphant',
      'Grateful',
      'Overjoyed',
      'Inspired',
      'Blissful',
      'Fulfilled',
      'Vibrant'
    ]
  };

  const moods = ['Poor', 'Fair', 'Good', 'Great', 'Excellent'];

  function updateMoodFactors(selectedMood, savedActiveMoodFactors = []) {
    // Clear existing mood factors
    moodFactorsContainer.innerHTML = '';

    // Add new mood factors
    moodFactorMap[selectedMood].forEach(factor => {
      const factorElement = document.createElement('div');
      factorElement.classList.add('mood-tag');
      factorElement.textContent = factor;
      
      // Check if this factor was previously active
      if (savedActiveMoodFactors.includes(factor)) {
        factorElement.classList.add('active');
      }
      
      // Add click toggle functionality
      factorElement.addEventListener('click', function() {
        this.classList.toggle('active');
        
        // Update localStorage with active mood factors
        const activeMoodFactors = Array.from(
          moodFactorsContainer.querySelectorAll('.mood-tag.active')
        ).map(tag => tag.textContent);
        
        localStorage.setItem('activeMoodFactors', JSON.stringify(activeMoodFactors));
        
        // Save mood entry
        saveMoodEntry(selectedMood);
      });

      moodFactorsContainer.appendChild(factorElement);
    });
  }

  function saveMoodEntry(selectedMood) {
    // Collect active mood factors
    const activeMoodFactors = Array.from(
      moodFactorsContainer.querySelectorAll('.mood-tag.active')
    ).map(tag => tag.textContent);

    // Save current mood to localStorage
    localStorage.setItem('currentMood', selectedMood);

    // Send data to backend
    fetch('/mySchedule/save-mood-entry/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken')
      },
      credentials: 'same-origin',
      body: JSON.stringify({
        mood_level: selectedMood,
        mood_factors: activeMoodFactors
      })
    })
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.json();
    })
    .then(data => {
      console.log('Mood entry saved successfully', data);
    })
    .catch(error => {
      console.error('Error saving mood entry:', error);
      alert('Failed to save mood entry. Please try again.');
    });
  }

  // CSRF Token retrieval function
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

  // Initialization function
  function initializeMoodMeter() {
    // Retrieve saved mood and active mood factors
    const savedMood = localStorage.getItem('currentMood') || 'Great';
    const savedActiveMoodFactors = JSON.parse(localStorage.getItem('activeMoodFactors')) || [];

    // Set mood slider to match saved mood
    const moodIndex = moods.indexOf(savedMood);
    moodSlider.value = moodIndex + 1;

    // Update mood text
    currentMood.textContent = savedMood;
    
    // Update mood factors
    updateMoodFactors(savedMood, savedActiveMoodFactors);
  }

  moodSlider.addEventListener('input', function() {
    const moodIndex = parseInt(this.value) - 1;
    const selectedMood = moods[moodIndex];
    
    // Update mood text
    currentMood.textContent = selectedMood;
    
    // Update mood factors (passing empty array to reset active states)
    updateMoodFactors(selectedMood);
    
    // Automatically save mood entry when slider changes
    saveMoodEntry(selectedMood);
  });

  // Initialize mood meter on page load
  initializeMoodMeter();
});