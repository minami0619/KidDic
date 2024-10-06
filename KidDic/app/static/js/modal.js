// function showModal() {
//     var modal = document.getElementById("myModal");
//     var modalImg = document.getElementById("modalImage");
//     var captionText = document.getElementById("caption");
//     var img = document.getElementById("quote-image");

//     modal.style.display = "block";  // モーダルを表示
//     modalImg.src = img.src;  // クリックされた画像をモーダルに表示
//     captionText.innerHTML = img.alt;  // 画像のalt属性をキャプションに表示
// }

// function closeModal() {
//     var modal = document.getElementById("myModal");
//     modal.style.display = "none";  // モーダルを非表示にする
// }


// function openModal() {
//     document.getElementById("quoteModal").style.display = "block";
// }

// function closeModal() {
//     document.getElementById("quoteModal").style.display = "none";
// }

// // モーダル外をクリックすると閉じる
// window.onclick = function(event) {
//     var modal = document.getElementById("quoteModal");
//     if (event.target == modal) {
//         modal.style.display = "none";
//     }
// }


// 画像を表示するためのモーダル
function showImageModal() {
    var modal = document.getElementById("myModal");
    var modalImg = document.getElementById("modalImage");
    var captionText = document.getElementById("caption");
    var img = document.getElementById("quote-image");

    modal.style.display = "block";  // モーダルを表示
    modalImg.src = img.src;  // クリックされた画像をモーダルに表示
    captionText.innerHTML = img.alt;  // 画像のalt属性をキャプションに表示
}

function closeImageModal() {
    var modal = document.getElementById("myModal");
    modal.style.display = "none";  // モーダルを非表示にする
}

document.querySelector(".fixed-add-btn").addEventListener("click", openQuoteModal);

// モーダルを開く関数
function openQuoteModal() {
    var modal = document.getElementById("quoteModal");
    var modalBackground = document.getElementById("modalBackground");
    modal.style.display = "block";
    modalBackground.style.display = "block"; // 背景も表示
}

// モーダルを閉じる関数
function closeQuoteModal() {
    var modal = document.getElementById("quoteModal");
    var modalBackground = document.getElementById("modalBackground");
    modal.style.display = "none";
    modalBackground.style.display = "none"; // 背景を非表示
}

// モーダル外をクリックして閉じる処理
window.onclick = function(event) {
    var modal = document.getElementById("quoteModal");
    var modalBackground = document.getElementById("modalBackground");
    if (event.target == modalBackground) {
        modal.style.display = "none";
        modalBackground.style.display = "none"; // 背景をクリックして閉じる
    }
}


// // 名言登録モーダルを開く関数
// function openQuoteModal() {
//     var modal = document.getElementById("quoteModal");
//     if (modal) {
//         modal.style.display = "block";
//     } else {
//         console.error("モーダルが見つかりません。IDが正しいか確認してください。");
//     }
// }

// // 名言登録モーダルを閉じる関数
// function closeQuoteModal() {
//     var modal = document.getElementById("quoteModal");
//     if (modal) {
//         modal.style.display = "none"; // モーダルを非表示
//         modalBackground.style.display = "none"; // 背景を非表示
//     }
// }

// // モーダル外をクリックして閉じる処理
// window.onclick = function(event) {
//     var modal = document.getElementById("quoteModal");
//     if (event.target == modal) {
//         modal.style.display = "none"; 
//         modalBackground.style.display = "none"; //  モーダル外をクリックすると閉じる
//     }
// }

