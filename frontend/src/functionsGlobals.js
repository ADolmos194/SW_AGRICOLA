import Swal from 'sweetalert2';

export function messagePopup(state, mensaje) {
    Swal.fire({
        //position: 'top-end',
        icon: state,
        title: mensaje,
        showConfirmButton: false,
    })
}

export async function messagePopupConfirm({message, text= '', titleAcept = 'OK', titleCancel = 'Cancel'}) {
    let response = await Swal.fire({
        title: message,
        text: text,
        icon: 'warning',
        showCancelButton: true,
        //confirmButtonColor: '#3085d6',
        //cancelButtonColor: '#d33',
        confirmButtonText: titleAcept,
        cancelButtonText: titleCancel
    })

    return response.isConfirmed ? true: false
}
