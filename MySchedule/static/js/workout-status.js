document.addEventListener('DOMContentLoaded', function() {
  const statusButtons = document.querySelectorAll('.workout-status');
  const caloriesStatCircle = document.querySelector('.stat-circle-burned');
  const calorieIntakeCircle = document.querySelector('.stat-circle-intake');
  const waterIntakeCircle = document.querySelector('.stat-circle-water');
  const proteinIntakeCircle = document.querySelector('.stat-circle-protein');

   // Mapping body goals to daily calorie burn targets
   const caloriesBurnTargets = {
    'victoria-secret-thin': 600, // Lower calorie burn for weight loss
    'slim': 800, // Moderate calorie burn for general fitness
    'athletic': 1200, // Higher calorie burn for active individuals
    'muscular': 1500, // High calorie burn for muscle building
    'sumo-wrestler': 2000 // Very high calorie burn
  };

  // Get the user's body goal from a data attribute on the body or a hidden input
  const bodyGoalElement = document.body.getAttribute('data-user-body-goal') || 
                          document.querySelector('input[name="user_body_goal"]');
  
  // Extract the body goal value
  const bodyGoal = bodyGoalElement ? 
    (typeof bodyGoalElement === 'string' ? bodyGoalElement : bodyGoalElement.value).toLowerCase() 
    : 'slim';
    
  const maxCalories = caloriesBurnTargets[bodyGoal] || caloriesBurnTargets['slim'];
  const maxCaloriesIntake = 2000;
  const maxWaterCups = 8;
  const maxProtein = 65;

  if (!caloriesStatCircle) {
    console.error('Could not find calories stat circle');
    return;
  }

  const caloriesNumber = caloriesStatCircle.querySelector('.stat-number');
  const caloriesSvgPath = caloriesStatCircle.querySelector('path:last-child');

  [caloriesSvgPath].forEach(path => {
    path.style.transition = 'stroke-dasharray 0.5s ease-in-out';
  });
  
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
    
    requestAnimationFrame(() => {
      caloriesSvgPath.setAttribute('stroke-dasharray', `${progressPercentage}, 100`);
    });
    
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
      checkDailyGoalsCompletion();
    });
  });
});

function checkDailyGoalsCompletion() {
  const totalCaloriesBurned = parseInt(caloriesNumber.textContent);
  const totalCaloriesIntake = parseInt(calorieIntakeCircle.querySelector('.stat-number').textContent);
  const currentWaterCups = parseInt(waterIntakeCircle.querySelector('.stat-number').textContent.split('/')[0]);
  const totalProteinIntake = parseInt(proteinIntakeCircle.querySelector('.stat-number').textContent);

  const isCaloriesBurnedGoalMet = totalCaloriesBurned >= maxCalories;
  const isCalorieIntakeGoalMet = totalCaloriesIntake >= maxCaloriesIntake;
  const isWaterGoalMet = currentWaterCups >= maxWaterCups;
  const isProteinGoalMet = totalProteinIntake >= maxProtein;

  if (isCaloriesBurnedGoalMet && isCalorieIntakeGoalMet && isWaterGoalMet && isProteinGoalMet) {
    // All goals met, mark the current date as completed
    markCurrentDateAsCompleted();
  }
}

function markCurrentDateAsCompleted() {
  const currentDate = new Date();
  const formattedDate = `${currentDate.getFullYear()}-${(currentDate.getMonth() + 1).toString().padStart(2, '0')}-${currentDate.getDate().toString().padStart(2, '0')}`;
  
  fetch('/mySchedule/mark-completed/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: `date=${formattedDate}`
  })
  .then(response => response.json())
  .then(data => {
    if (data.status === 'success') {
      // Update the current date in the calendar to have success class
      const currentDayElement = document.querySelector('.calendar-day-today');
      if (currentDayElement) {
        currentDayElement.classList.remove('calendar-day-today');
        currentDayElement.classList.add('calendar-day-today-success');
      }
    }
  })
  .catch(error => {
    console.error('Error marking date as completed:', error);
  });
}