document.addEventListener('DOMContentLoaded', function() {
  const form = document.querySelector('form');
  const avatarUpload = document.getElementById('avatarB-upload');
  const avatarImage = document.getElementById('avatarBImage').querySelector('img');
  const uploadTriggerElements = [
      document.getElementById("avatarBImage"), 
      document.getElementById("avatarBCircle")
  ];

  // Trigger file upload when either the profile image or circle icon is clicked
  uploadTriggerElements.forEach(element => {
      element.addEventListener("click", function () {
          avatarUpload.click();
      });
  });

  avatarUpload.addEventListener('change', function(event) {
      const file = event.target.files[0];
      if (file) {
          const reader = new FileReader();
          
          reader.onload = function(e) {
              // Create an off-screen image to get dimensions
              const img = new Image();
              img.onload = function() {
                  // Create a canvas to crop and resize the image
                  const canvas = document.createElement('canvas');
                  const ctx = canvas.getContext('2d');
                  
                  // Set canvas to the desired output size (match your circular frame)
                  const targetSize = 207; 
                  canvas.width = targetSize;
                  canvas.height = targetSize;
                  
                  // Calculate scaling and cropping
                  const aspectRatio = img.width / img.height;
                  let sourceWidth, sourceHeight, sourceX, sourceY;
                  
                  if (aspectRatio > 1) {
                      // Landscape image
                      sourceHeight = img.height;
                      sourceWidth = sourceHeight;
                      sourceX = (img.width - sourceHeight) / 2;
                      sourceY = 0;
                  } else {
                      // Portrait image
                      sourceWidth = img.width;
                      sourceHeight = sourceWidth;
                      sourceX = 0;
                      sourceY = (img.height - sourceWidth) / 2;
                  }
                  
                  // Draw the cropped and scaled image
                  ctx.drawImage(
                      img, 
                      sourceX, sourceY, sourceWidth, sourceHeight, 
                      0, 0, targetSize, targetSize 
                  );
                  
                  // Convert canvas to blob and append to form
                  canvas.toBlob(function(blob) {
                    // Create a new FormData object and append the blob
                    const formData = new FormData(form);
                    formData.append('profile_photo', blob, 'profile_photo.jpg');
                    
                    // Optional: If you want to send the image immediately
                    fetch(form.action, {
                      method: 'POST',
                      body: formData,
                      headers: {
                        'X-Requested-With': 'XMLHttpRequest',
                        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                      }
                    })
                      .then(response => response.json())
                      .then(data => {
                          if (data.status === 'success') {
                              console.log('Profile photo uploaded successfully');
                              // Optionally update UI or show success message
                          } else {
                              console.error('Error uploading profile photo');
                              // Optionally show error message
                          }
                      })
                      .catch(error => {
                          console.error('Error:', error);
                      });
                  }, 'image/jpeg');
                  
                  // Set the canvas image as the new avatar
                  avatarImage.src = canvas.toDataURL('image/jpeg');
              };
              
              // Set the source of the image for processing
              img.src = e.target.result;
          };
          
          // Read the uploaded file
          reader.readAsDataURL(file);
      }
  });
});