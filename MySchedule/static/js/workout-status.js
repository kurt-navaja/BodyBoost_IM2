document.addEventListener('DOMContentLoaded', function() {
  const statusButtons = document.querySelectorAll('.workout-status');

  statusButtons.forEach(button => {
    button.addEventListener('click', function() {
      const isComplete = this.classList.contains('complete');
      
      this.classList.add('animating');
      
      setTimeout(() => {
        this.classList.remove('animating');
      }, 300);

      if (isComplete) {
        this.classList.remove('complete');
        this.classList.add('pending');
        this.textContent = 'Pending';
      } else {
        this.classList.remove('pending');
        this.classList.add('complete');
        this.textContent = 'Complete';
      }

      const workoutId = this.closest('.workout-item').querySelector('h5').textContent;
      localStorage.setItem(`workout-${workoutId}`, isComplete ? 'pending' : 'complete');
    });
  });

  statusButtons.forEach(button => {
    const workoutId = button.closest('.workout-item').querySelector('h5').textContent;
    const savedStatus = localStorage.getItem(`workout-${workoutId}`);
    if (savedStatus) {
      button.classList.remove('complete', 'pending');
      button.classList.add(savedStatus);
      button.textContent = savedStatus.charAt(0).toUpperCase() + savedStatus.slice(1);
    }
  });
});