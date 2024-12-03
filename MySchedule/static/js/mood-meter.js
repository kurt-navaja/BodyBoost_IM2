document.addEventListener('DOMContentLoaded', function() {
  const moodSlider = document.getElementById('moodSlider');
  const currentMood = document.querySelector('.current-mood');

  const moods = ['Poor', 'Fair', 'Good', 'Great', 'Excellent'];

  moodSlider.addEventListener('input', function() {
    const moodIndex = parseInt(this.value) - 1;
    currentMood.textContent = moods[moodIndex];
  });

  // Toggle mood factors
  document.querySelectorAll('.mood-tag').forEach(tag => {
    tag.addEventListener('click', function() {
      this.classList.toggle('active');
    });
  });
});