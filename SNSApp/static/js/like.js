document.addEventListener('DOMContentLoaded', function() {
    var likeBtns = document.getElementsByClassName('likeBtn');
    Array.from(likeBtns).forEach(function(btn) {
        var form = btn.closest('form');
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            var url = form.action;
            var formData = new FormData(form);

            fetch(url, {
                method: 'POST',
                body: formData,
                headers: { 'X-Requested': 'XMLHttpRequesr' }
            })
            .then(response => response.json())
            .then(data => {
                btn.classList.toggle('liked');
                var icon = btn.querySelector('i');
                if (data.is_liked) {
                    icon.classList.replace('fa-regular', 'fa-solid');
                } else {
                    icon.classList.replace('fa-solid', 'fa-regular');
                }
            })
            .catch(error => console.error('エラー:', error));
        });
    });
}, false);
