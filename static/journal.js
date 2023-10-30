function showModal(note) {
    var modal = document.getElementById("myModal");
    var modalContent = document.getElementById("modalContent");
    modalContent.innerText = note;
    modal.classList.add('modal-open');
}

function closeModal() {
    var modal = document.getElementById("myModal");
    modal.classList.remove('modal-open');
}

function deleteTrade(event, tradeId) {
    event.preventDefault();

    // Confirm if the user wants to delete the trade
    var confirmation = confirm("Are you sure you want to delete this trade?");

    if (!confirmation) return;

    // Send an AJAX request to delete the trade
    fetch(`/delete_trade/${tradeId}`, {
        method: 'DELETE'
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            // If successful, animate and remove the row
            let row = event.target.closest('tr');
            row.style.opacity = '0';
            setTimeout(() => {
                row.remove();
            }, 300); // 300ms matches the animation duration
        } else {
            alert("There was an error deleting the trade.");
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert("There was an error deleting the trade.");
    });
}
