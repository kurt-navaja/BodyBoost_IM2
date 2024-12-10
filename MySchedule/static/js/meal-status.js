document.addEventListener('DOMContentLoaded', () => {
  const mealItems = document.querySelectorAll('.meal-item');
  const calorieIntakeCircle = document.querySelector('.stat-circle-intake');
  const proteinIntakeCircle = document.querySelector('.stat-circle-protein');
  const caloriesBurnedCircle = document.querySelector('.stat-circle-burned');

  // Mapping body goals to daily calorie and protein targets
  const nutritionTargets = {
    'victoria-secret-thin': {
      calories: 1700,
      protein: 50 // Lower protein for weight loss
    },
    'slim': {
      calories: 2000,
      protein: 65 // Moderate protein for general fitness
    },
    'athletic': {
      calories: 2400,
      protein: 90 // Higher protein for active individuals
    },
    'muscular': {
      calories: 3100,
      protein: 130 // High protein for muscle building
    },
    'sumo-wrestler': {
      calories: 4000,
      protein: 180 // Very high protein and calorie intake
    }
  };

  // Get the user's body goal from a data attribute on the body or a hidden input
  const bodyGoalElement = document.body.getAttribute('data-user-body-goal') || 
                          document.querySelector('input[name="user_body_goal"]');
  
  // Extract the body goal value
  const bodyGoal = bodyGoalElement ? 
    (typeof bodyGoalElement === 'string' ? bodyGoalElement : bodyGoalElement.value).toLowerCase() 
    : 'slim';

  // Set max calories and protein based on body goal, defaulting to 'slim' if not found
  const { calories: maxCalories, protein: maxProtein } = nutritionTargets[bodyGoal] || nutritionTargets['slim'];

  const maxCaloriesBurned = 1000; // Adjust based on user's daily calorie burn goal

  if (!calorieIntakeCircle || !proteinIntakeCircle) {
    console.error('Could not find intake stat circles');
    return;
  }

  const caloriesNumber = calorieIntakeCircle.querySelector('.stat-number');
  const proteinNumber = proteinIntakeCircle.querySelector('.stat-number');
  const caloriesSvgPath = calorieIntakeCircle.querySelector('path:last-child');
  const proteinSvgPath = proteinIntakeCircle.querySelector('path:last-child');

  // Add smooth transition to SVG paths
  [caloriesSvgPath, proteinSvgPath].forEach(path => {
    path.style.transition = 'stroke-dasharray 0.5s ease-in-out';
  });

  // Initialize totals from localStorage
  let totalCaloriesIntake = parseInt(localStorage.getItem('totalCaloriesIntake') || '0');
  let totalProteinIntake = parseInt(localStorage.getItem('totalProteinIntake') || '0');
  
  // Load previously selected meals from localStorage
  const selectedMeals = JSON.parse(localStorage.getItem('selectedMeals') || '[]');

  // Function to update number color based on progress
  function updateIntakeNumberColor(numberElement, currentValue, maxValue) {
    numberElement.style.transition = 'color 0.5s ease';
    
    if (currentValue >= maxValue) {
      numberElement.style.color = '#00f863'; // Smooth green when max reached
    } else {
      numberElement.style.color = ''; // Return to default color
    }
  }

  // Initial setup of calorie and protein displays
  function setupIntakeDisplay() {
    if (caloriesNumber) {
      caloriesNumber.textContent = totalCaloriesIntake;
      const caloriesProgressPercentage = Math.min((totalCaloriesIntake / maxCalories) * 100, 100);
      
      // Smooth animation
      requestAnimationFrame(() => {
        caloriesSvgPath.setAttribute('stroke-dasharray', `${caloriesProgressPercentage}, 100`);
      });
      
      updateIntakeNumberColor(caloriesNumber, totalCaloriesIntake, maxCalories);
    }

    if (proteinNumber) {
      proteinNumber.textContent = `${totalProteinIntake}g`;
      const proteinProgressPercentage = Math.min((totalProteinIntake / maxProtein) * 100, 100);
      
      // Smooth animation
      requestAnimationFrame(() => {
        proteinSvgPath.setAttribute('stroke-dasharray', `${proteinProgressPercentage}, 100`);
      });
      
      updateIntakeNumberColor(proteinNumber, totalProteinIntake, maxProtein);
    }
  }

  // Restore selected state on page load
  selectedMeals.forEach(mealIndex => {
    if (mealItems[mealIndex]) {
      const mealItem = mealItems[mealIndex];
      mealItem.classList.add('selected');
      
      // Extract calories and protein from the meal item
      const caloriesMatch = mealItem.textContent.match(/(\d+) cal/);
      const proteinMacro = mealItem.querySelector('.meal-macros span:first-child');
      const proteinMatch = proteinMacro ? proteinMacro.textContent.match(/(\d+)/) : null;
      
      if (caloriesMatch && proteinMatch) {
        const mealCalories = parseInt(caloriesMatch[1]);
        const mealProtein = parseInt(proteinMatch[1]);
        
        totalCaloriesIntake += mealCalories;
        totalProteinIntake += mealProtein;
      }
    }
  });

  // Setup initial display after restoring selections
  setupIntakeDisplay();

  // Add reset functionality to calorie and protein numbers
  [caloriesNumber, proteinNumber].forEach(numberElement => {
    numberElement.style.cursor = 'pointer';
    numberElement.style.transition = 'color 0.3s ease';

    numberElement.addEventListener('click', () => {
      // Reset values
      totalCaloriesIntake = 0;
      totalProteinIntake = 0;
      
      // Clear localStorage
      localStorage.removeItem('totalCaloriesIntake');
      localStorage.removeItem('totalProteinIntake');
      localStorage.removeItem('selectedMeals');
      
      // Reset display
      setupIntakeDisplay();
      
      // Reset meal selections
      mealItems.forEach(item => {
        item.classList.remove('selected');
      });
    });
  });

  // Add click event to meal items
  mealItems.forEach((item, index) => {
    item.addEventListener('click', () => {
      // Extract calories and protein from the meal item
      const caloriesMatch = item.textContent.match(/(\d+) cal/);
      const proteinMacro = item.querySelector('.meal-macros span:first-child');
      const proteinMatch = proteinMacro ? proteinMacro.textContent.match(/(\d+)/) : null;
      
      if (caloriesMatch && proteinMatch) {
        const mealCalories = parseInt(caloriesMatch[1]);
        const mealProtein = parseInt(proteinMatch[1]);
        
        // Toggle selected state
        if (item.classList.contains('selected')) {
          // Removing selection
          item.classList.remove('selected');
          totalCaloriesIntake -= mealCalories;
          totalProteinIntake -= mealProtein;
        } else {
          // Adding selection
          item.classList.add('selected');
          totalCaloriesIntake += mealCalories;
          totalProteinIntake += mealProtein;
        }
        
        // Ensure we don't go below 0
        totalCaloriesIntake = Math.max(0, totalCaloriesIntake);
        totalProteinIntake = Math.max(0, totalProteinIntake);
        
        // Update display
        setupIntakeDisplay();
        
        // Update localStorage
        localStorage.setItem('totalCaloriesIntake', totalCaloriesIntake.toString());
        localStorage.setItem('totalProteinIntake', totalProteinIntake.toString());
        
        // Update selected meals
        const currentSelectedMeals = Array.from(document.querySelectorAll('.meal-item.selected'))
          .map(selectedItem => Array.from(mealItems).indexOf(selectedItem));
        
        localStorage.setItem('selectedMeals', JSON.stringify(currentSelectedMeals));
      }
      checkDailyGoalsCompletion();
    });
  });

  // Water intake section - updated with improved functionality
  const waterIntakeCircle = document.querySelector('.stat-circle-water');
  const maxWaterCups = 8;

  if (!waterIntakeCircle) {
    console.error('Could not find water intake stat circle');
    return;
  }

  const waterNumber = waterIntakeCircle.querySelector('.stat-number');
  const waterSvgPath = waterIntakeCircle.querySelector('path:last-child');

  // Add smooth transition to SVG path
  waterSvgPath.style.transition = 'stroke-dasharray 0.5s ease-in-out';

  // Initialize water intake from localStorage
  let currentWaterCups = parseInt(localStorage.getItem('totalWaterIntake') || '0');

  // Function to update water intake display
  function setupWaterIntakeDisplay() {
    if (waterNumber) {
      waterNumber.textContent = `${currentWaterCups}/${maxWaterCups}`;
      
      // Calculate progress percentage
      const waterProgressPercentage = Math.min((currentWaterCups / maxWaterCups) * 100, 100);
      
      // Smooth animation
      requestAnimationFrame(() => {
        waterSvgPath.setAttribute('stroke-dasharray', `${waterProgressPercentage}, 100`);
      });
      
      // Update color when goal is reached
      waterNumber.style.transition = 'color 0.5s ease';
      if (currentWaterCups >= maxWaterCups) {
        waterNumber.style.color = '#00f863'; // Smooth green when max reached
      } else {
        waterNumber.style.color = ''; // Return to default color
      }
    }
  }

  // Make water number clickable and interactive
  if (waterNumber) {
    waterNumber.style.cursor = 'pointer';
    waterNumber.style.transition = 'color 0.3s ease';

    waterNumber.addEventListener('click', () => {
      // Increment water intake
      if (currentWaterCups < maxWaterCups) {
        currentWaterCups++;
      } else {
        // Reset to 0 if max is reached
        currentWaterCups = 0;
      }

      // Update localStorage
      localStorage.setItem('totalWaterIntake', currentWaterCups.toString());

      // Update display
      setupWaterIntakeDisplay();
      checkDailyGoalsCompletion();
    });

    // Reset functionality when double-clicked
    waterNumber.addEventListener('dblclick', () => {
      currentWaterCups = 0;
      localStorage.removeItem('totalWaterIntake');
      setupWaterIntakeDisplay();
    });
  }

  // Initial setup on page load
  setupWaterIntakeDisplay();
});

function checkDailyGoalsCompletion() {
  const caloriesNumber = document.querySelector('.stat-circle-intake .stat-number');
  const proteinNumber = document.querySelector('.stat-circle-protein .stat-number');
  const waterNumber = document.querySelector('.stat-circle-water .stat-number');
  const caloriesBurnedNumber = document.querySelector('.stat-circle-burned .stat-number');

  // Check if all required elements exist
  if (!caloriesNumber || !proteinNumber || !waterNumber || !caloriesBurnedNumber) {
    console.error('One or more goal tracking elements are missing');
    return;
  }

  const maxCalories = 2000;
  const maxProtein = 65;
  const maxWaterCups = 8;
  const maxCaloriesBurned = 1000;

  const totalCaloriesIntake = parseInt(caloriesNumber.textContent);
  const totalProteinIntake = parseInt(proteinNumber.textContent);
  const currentWaterCups = parseInt(waterNumber.textContent.split('/')[0]);
  const totalCaloriesBurned = parseInt(caloriesBurnedNumber.textContent);

  console.log('Goal Check:', {
    caloriesIntake: { current: totalCaloriesIntake, max: maxCalories },
    proteinIntake: { current: totalProteinIntake, max: maxProtein },
    waterCups: { current: currentWaterCups, max: maxWaterCups },
    caloriesBurned: { current: totalCaloriesBurned, max: maxCaloriesBurned }
  });

  const isCalorieGoalMet = totalCaloriesIntake >= maxCalories;
  const isProteinGoalMet = totalProteinIntake >= maxProtein;
  const isWaterGoalMet = currentWaterCups >= maxWaterCups;
  const isCaloriesBurnedGoalMet = totalCaloriesBurned >= maxCaloriesBurned;

  console.log('Goal Status:', {
    caloriesIntake: isCalorieGoalMet,
    proteinIntake: isProteinGoalMet,
    waterCups: isWaterGoalMet,
    caloriesBurned: isCaloriesBurnedGoalMet
  });

  if (isCalorieGoalMet && isProteinGoalMet && isWaterGoalMet && isCaloriesBurnedGoalMet) {
    console.log('All daily goals met, attempting to mark date as completed');
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