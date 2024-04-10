document.getElementById('refresh-button').addEventListener('click', function() {
    location.reload();
});

document.getElementById('delete-button').addEventListener('click', function() {
    fetch('/delete', {method: 'POST'})
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            location.reload();
        } else {
            alert('Error deleting table contents');
        }
    });
});