let uploadButton = document.getElementById("upload-button");
let chosenImage = document.getElementById("chosen-image");
let fileName = document.getElementById("file-name");
let uploadForm = document.getElementById("upload-form");
let btnInParking = document.getElementById("btnInParking");
let licenePlate =  document.getElementById('licenePlate')
uploadButton.onchange = () => {
    let reader = new FileReader();
    reader.readAsDataURL(uploadButton.files[0]);
    reader.onload = () => {
        chosenImage.setAttribute("src", reader.result);
        // uploadForm.submit();
        const formData = new FormData();
        formData.append('file', uploadButton.files[0]);
        console.log(uploadButton.files[0]);
        fetch('/uploads', {
            method: 'POST',
            body: formData
        })
            .then(response => response.json())
            .then(data => {
                if (data.result) {
                    document.getElementById('licenePlate').value = data.result;
                } else {
                    document.getElementById('licenePlate').value = '';
                }
            })
            .catch(error => {
                document.getElementById('licenePlate').value = '';
            });
    }
}


async function handleButtonInParking() {
    const url = 'http://localhost:8010/api/parkingTurn/createPakingTurnWithoutZoneAndPosition';

    try {
        // Gửi yêu cầu fetch
        const formData = new FormData();
        formData.append('image', uploadButton.files[0]);
        console.log(uploadButton.files[0]);
        formData.append('licenePlate',licenePlate.value);
        const response = await fetch(url, {
            method: 'POST', // Hoặc 'POST', 'PUT', v.v. tùy thuộc vào yêu cầu của bạn
            body: formData
        });

        // Kiểm tra xem yêu cầu có thành công không
        if (!response.ok) {
            throw new Error('Network response was not ok ' + response.statusText);
        }

        // Chuyển đổi dữ liệu phản hồi thành JSON
        const data = await response.json();
        console.log(data); // Xử lý dữ liệu JSON tại đây (ví dụ: hiển thị trên giao diện)

    } catch (error) {
        console.error('Fetch error: ', error);
    }
}

// Đợi DOM được tải đầy đủ rồi thêm sự kiện lắng nghe vào nút
btnInParking.addEventListener('click', handleButtonInParking);