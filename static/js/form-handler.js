document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    const textarea = document.getElementById('message');
    
    // Create container div for alert
    const errorMessage = document.createElement('div');
    errorMessage.className = 'flex items-center p-4 mb-4 text-sm text-red-800 border border-red-300 rounded-lg bg-red-50 dark:bg-gray-800 dark:text-red-400 dark:border-red-800 hidden';
    errorMessage.setAttribute('role', 'alert');
    
    // Create and add the SVG icon
    errorMessage.innerHTML = `
        <svg class="flex-shrink-0 inline w-4 h-4 me-3" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 20 20">
            <path d="M10 .5a9.5 9.5 0 1 0 9.5 9.5A9.51 9.51 0 0 0 10 .5ZM9.5 4a1.5 1.5 0 1 1 0 3 1.5 1.5 0 0 1 0-3ZM12 15H8a1 1 0 0 1 0-2h1v-3H8a1 1 0 0 1 0-2h2a1 1 0 0 1 1 1v4h1a1 1 0 0 1 0 2Z"/>
        </svg>
        <span class="sr-only">Info</span>
        <div>
            <span class="font-medium">Cannot submit empty question!</span> Please enter your question and try again.
        </div>
    `;
    
    textarea.parentNode.appendChild(errorMessage);
    
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
            
            form.submit();
        }
    });
});