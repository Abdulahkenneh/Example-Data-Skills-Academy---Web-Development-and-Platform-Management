document.addEventListener("DOMContentLoaded", function() {
    document.querySelectorAll('.post-link').forEach(function(postLink) {
        postLink.addEventListener('click', function(event) {
            event.preventDefault();
            const postId = this.getAttribute('data-post-id');
            fetch(`/post/?post_id=${postId}`, {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                document.querySelector('.post-title').textContent = data.title;
                document.querySelector('.post-content').innerHTML = `<p>${data.content}</p>`;
                document.querySelector('.post-user').textContent = `by ${data.user}`;
                document.querySelector('.post-date').textContent = data.created_at;
                document.querySelector('.post-id').textContent = data.postId;
          
           
            })
            .catch(error => console.error('Error fetching post:', error));
        });
    });
});
