document.addEventListener('DOMContentLoaded', function() {
  const saveButton = document.querySelector('.mac-book-air1-next');
  const form = document.querySelector('form');

  const createMessageContainer = () => {
      const container = document.createElement('div');
      container.style.position = 'fixed';
      container.style.top = '150px';
      container.style.left = '52%';
      container.style.transform = 'translateX(-50%)';
      container.style.padding = '10px';
      container.style.borderRadius = '8px';
      container.style.zIndex = '1000';
      container.style.color = 'white';
      container.style.fontWeight = 'bold';
      container.style.display = 'none';
      document.body.appendChild(container);
      return container;
  };

  const messageContainer = createMessageContainer();

  const showMessage = (message, isSuccess) => {
      messageContainer.textContent = message;
      messageContainer.style.backgroundColor = isSuccess ? '#4CAF50' : '#F44336';
      messageContainer.style.display = 'block';
      
      setTimeout(() => {
          messageContainer.style.display = 'none';
      }, 5000);
  };

  saveButton.addEventListener('click', function(e) {
      e.preventDefault();

      const formData = new FormData(form);

      fetch(form.action, {
          method: 'POST',
          body: formData,
          headers: {
              'X-Requested-With': 'XMLHttpRequest',
              'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
          }
      })
      .then(response => {
          // Always try to parse as JSON
          return response.json().then(data => {
              return { status: response.ok, data: data };
          }).catch(() => {
              return { 
                  status: false, 
                  data: { message: 'Unable to parse server response' } 
              };
          });
      })
      .then(({ status, data }) => {
          if (status) {
              // Success case
              showMessage(data.message || 'Account settings saved successfully!', true);
          } else {
              // Error case
              showMessage(data.message || 'An error occurred while saving settings', false);
          }
      })
      .catch(error => {
          console.error('Error:', error);
          showMessage('An unexpected error occurred', false);
      });
  });
});