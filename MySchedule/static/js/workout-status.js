document.addEventListener('DOMContentLoaded', function() {
  const statusButtons = document.querySelectorAll('.workout-status');
  const caloriesStatCircle = document.querySelector('.stat-circle-burned');
  const maxCalories = 1000;

  if (!caloriesStatCircle) {
    console.error('Could not find calories stat circle');
    return;
  }

  const caloriesNumber = caloriesStatCircle.querySelector('.stat-number');
  const caloriesSvgPath = caloriesStatCircle.querySelector('path:last-child');
  
  // Initialize total calories burned, starting from localStorage
  let totalCaloriesBurned = parseInt(localStorage.getItem('totalCaloriesBurned') || '0');
  
  // Initialize workout statuses from localStorage
  const savedWorkoutStatuses = JSON.parse(localStorage.getItem('workoutStatuses') || '{}');

  // Function to update calories number color based on progress
  function updateCaloriesNumberColor() {
    caloriesNumber.style.transition = 'color 0.5s ease';
    
    if (totalCaloriesBurned >= maxCalories) {
      caloriesNumber.style.color = '#00f863'; // Smooth green when max calories reached
    } else {
      caloriesNumber.style.color = ''; // Return to default color
    }
  }

  // Update calories display and circle progress on page load
  if (caloriesNumber) {
    caloriesNumber.textContent = totalCaloriesBurned;
    
    // Add reset hover effect
    caloriesNumber.style.cursor = 'pointer';
    caloriesNumber.style.transition = 'color 0.3s ease';
    
    caloriesNumber.addEventListener('mouseenter', function() {
      if (totalCaloriesBurned < maxCalories) {
        this.style.color = '#ff4444'; // Smooth red on hover (only if not max calories)
      }
    });
    
    caloriesNumber.addEventListener('mouseleave', function() {
      updateCaloriesNumberColor();
    });

    // Reset functionality on click
    caloriesNumber.addEventListener('click', function() {
      // Reset calories
      totalCaloriesBurned = 0;
      localStorage.setItem('totalCaloriesBurned', '0');
      
      // Reset calories display
      this.textContent = '0';
      updateCaloriesNumberColor();
      
      // Reset SVG path
      if (caloriesSvgPath) {
        caloriesSvgPath.setAttribute('stroke-dasharray', '0, 100');
      }
      
      // Reset all workout statuses
      statusButtons.forEach(button => {
        button.classList.remove('complete');
        button.classList.add('pending');
        button.textContent = 'Pending';
      });
      
      // Clear saved statuses
      localStorage.removeItem('workoutStatuses');
    });
    
    // Calculate and set circle progress based on total calories burned
    const progressPercentage = Math.min((totalCaloriesBurned / maxCalories) * 100, 100);
    const dashArrayValue = `${progressPercentage}, 100`;
    
    caloriesSvgPath.setAttribute('stroke-dasharray', dashArrayValue);
    
    // Set initial color based on calories
    updateCaloriesNumberColor();
  }

  statusButtons.forEach(button => {
    const workoutItem = button.closest('.workout-item');
    const workoutDetails = workoutItem.querySelector('.workout-details p');
    const caloriesMatch = workoutDetails.textContent.match(/(\d+) calories/);

    // Restore previous status if exists
    const workoutKey = workoutDetails.textContent.trim();
    if (savedWorkoutStatuses[workoutKey]) {
      button.classList.remove('pending');
      button.classList.add('complete');
      button.textContent = 'Complete';
    }

    button.addEventListener('click', function() {
      if (caloriesMatch) {
        const workoutCalories = parseInt(caloriesMatch[1]);
        
        // Toggle between pending and complete
        if (this.classList.contains('complete')) {
          // Clicking a completed workout removes calories
          totalCaloriesBurned -= workoutCalories;
          this.classList.remove('complete');
          this.classList.add('pending');
          this.textContent = 'Pending';
          
          // Remove from saved statuses
          delete savedWorkoutStatuses[workoutKey];
        } else {
          // Clicking a pending workout adds calories
          totalCaloriesBurned += workoutCalories;
          this.classList.remove('pending');
          this.classList.add('complete');
          this.textContent = 'Complete';
          
          // Save status
          savedWorkoutStatuses[workoutKey] = true;
        }
        
        // Update calories display
        if (caloriesNumber) {
          caloriesNumber.textContent = totalCaloriesBurned;
          updateCaloriesNumberColor();
        }
        
        // Save to localStorage
        localStorage.setItem('totalCaloriesBurned', totalCaloriesBurned.toString());
        localStorage.setItem('workoutStatuses', JSON.stringify(savedWorkoutStatuses));
        
        // Update calories circle
        const progressPercentage = Math.min((totalCaloriesBurned / maxCalories) * 100, 100);
        const dashArrayValue = `${progressPercentage}, 100`;
        
        if (caloriesSvgPath) {
          caloriesSvgPath.setAttribute('stroke-dasharray', dashArrayValue);
        }
      }
    });
  });
});