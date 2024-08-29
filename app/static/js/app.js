function notificationClose() {
    var closeButton = document.querySelector('.popup-notification-close');
    closeButton.addEventListener('click', function() {
        var notification = this.closest('.notification-popup');
        notification.remove();
    });
};
