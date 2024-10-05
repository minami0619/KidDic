function showModal() {
    var modal = document.getElementById("myModal");
    var modalImg = document.getElementById("modalImage");
    var captionText = document.getElementById("caption");
    var img = document.getElementById("quote-image");

    modal.style.display = "block";  // モーダルを表示
    modalImg.src = img.src;  // クリックされた画像をモーダルに表示
    captionText.innerHTML = img.alt;  // 画像のalt属性をキャプションに表示
}

function closeModal() {
    var modal = document.getElementById("myModal");
    modal.style.display = "none";  // モーダルを非表示にする
}


function openModal() {
    document.getElementById("quoteModal").style.display = "block";
}

function closeModal() {
    document.getElementById("quoteModal").style.display = "none";
}

// モーダル外をクリックすると閉じる
window.onclick = function(event) {
    var modal = document.getElementById("quoteModal");
    if (event.target == modal) {
        modal.style.display = "none";
    }
}
