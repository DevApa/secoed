function notification(title, message, icon) {
    Swal.fire({
        title: title,
        text: message,
        icon: icon,
        showConfirmButton: false,
        timer:3000
    });
}