// Wait for the DOM to be fully loaded before attaching event listeners
document.addEventListener('DOMContentLoaded', function() {
    // Get references to key DOM elements
    const form = document.querySelector('form');
    const textarea = document.getElementById('message');
    const progressBar = document.getElementById('progress-bar');
    
    // Create and style the error message element that appears when submission is empty
    const errorMessage = document.createElement('div');
    errorMessage.className = 'mt-4 flex items-start gap-3 p-4 mb-4 text-sm rounded-lg border bg-gray-800 hidden';
    errorMessage.setAttribute('role', 'alert');
    
    // Apply styles directly to ensure consistent error appearance
    errorMessage.style.color = 'rgb(248 113 113)';
    errorMessage.style.borderColor = 'rgb(248 113 113)';
    
    // Set up the error message HTML structure with icon and text
    errorMessage.innerHTML = `
        <svg class="flex-shrink-0 w-4 h-4 mt-0.5" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 20 20">
            <path d="M10 .5a9.5 9.5 0 1 0 9.5 9.5A9.51 9.51 0 0 0 10 .5ZM9.5 4a1.5 1.5 0 1 1 0 3 1.5 1.5 0 0 1 0-3ZM12 15H8a1 1 0 0 1 0-2h1v-3H8a1 1 0 0 1 0-2h2a1 1 0 0 1 1 1v4h1a1 1 0 0 1 0 2Z"/>
        </svg>
        <div class="flex-1">
            <span class="font-medium">Cannot submit empty question!</span> Please enter your question and try again.
        </div>
    `;
    
    // Ensure error icon color matches the text
    const svg = errorMessage.querySelector('svg');
    if (svg) {
        svg.style.color = 'rgb(248 113 113)';
    }
    
    // Add error message to the DOM
    textarea.parentNode.appendChild(errorMessage);
    
    // Function to handle form submission
    function submitForm() {
        if (!textarea.value.trim()) {
            errorMessage.classList.remove('hidden');
            setTimeout(() => {
                errorMessage.classList.add('hidden');
            }, 3000);
            return false;
        }
        
        // Show progress bar
        if (progressBar) {
            progressBar.classList.remove('hidden');
        }
        
        // Store submission state
        sessionStorage.setItem('formSubmitted', 'true');
        return true;
    }
    
    // Handle form submissions (button click)
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        if (submitForm()) {
            this.submit();
        }
    });
    
    // Handle Enter key submissions
    textarea.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            if (submitForm()) {
                form.submit();
            }
        }
    });
    
    // Clear submission state on page load
    if (sessionStorage.getItem('formSubmitted')) {
        sessionStorage.removeItem('formSubmitted');
        if (progressBar) {
            progressBar.classList.add('hidden');
        }
    }
});