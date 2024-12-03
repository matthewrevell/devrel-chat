document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    const textarea = document.getElementById('message');
    const progressBar = document.getElementById('progress-bar');
    
    // Error message setup
    const errorMessage = document.createElement('div');
    errorMessage.className = 'mt-4 flex items-start gap-3 p-4 mb-4 text-sm rounded-lg border bg-gray-800 hidden';
    errorMessage.setAttribute('role', 'alert');
    
    // Set styles directly
    errorMessage.style.color = 'rgb(248 113 113)';
    errorMessage.style.borderColor = 'rgb(248 113 113)';
    
    errorMessage.innerHTML = `
        <svg class="flex-shrink-0 w-4 h-4 mt-0.5" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 20 20">
            <path d="M10 .5a9.5 9.5 0 1 0 9.5 9.5A9.51 9.51 0 0 0 10 .5ZM9.5 4a1.5 1.5 0 1 1 0 3 1.5 1.5 0 0 1 0-3ZM12 15H8a1 1 0 0 1 0-2h1v-3H8a1 1 0 0 1 0-2h2a1 1 0 0 1 1 1v4h1a1 1 0 0 1 0 2Z"/>
        </svg>
        <div class="flex-1">
            <span class="font-medium">Cannot submit empty question!</span> Please enter your question and try again.
        </div>
    `;
    
    const svg = errorMessage.querySelector('svg');
    if (svg) {
        svg.style.color = 'rgb(248 113 113)';
    }
    
    textarea.parentNode.appendChild(errorMessage);
    
    // Add keyframe animation
    const style = document.createElement('style');
    style.textContent = `
        @keyframes loading {
            0% { width: 0% }
            50% { width: 100% }
            100% { width: 0% }
        }
    `;
    document.head.appendChild(style);
    
    // Check and clear submission state
    if (sessionStorage.getItem('formSubmitted')) {
        sessionStorage.removeItem('formSubmitted');
        progressBar.classList.add('hidden');
    }
    
    textarea.addEventListener('keydown', function(e) {
        if (e.key === 'Enter') {
            if (e.shiftKey) {
                return;
            }
            
            e.preventDefault();
            
            if (!textarea.value.trim()) {
                errorMessage.classList.remove('hidden');
                
                setTimeout(() => {
                    errorMessage.classList.add('hidden');
                }, 3000);
                
                return;
            }
            
            // Show progress bar and submit form
            progressBar.classList.remove('hidden');
            sessionStorage.setItem('formSubmitted', 'true');
            form.submit();
        }
    });
});