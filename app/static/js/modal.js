// 画像を表示するためのモーダル
function showImageModal(imgElement) {
    var modal = document.getElementById("myModalImage");
    var modalImg = document.getElementById("modalImage");
    var captionText = document.getElementById("caption");

    // 引数から画像のsrcを取得する
    modal.style.display = "block";
    modalImg.src = imgElement.src;  // imgElementからsrcを取得
    modalImg.alt = imgElement.alt;  // imgElementからaltを取得
    captionText.innerHTML = imgElement.alt;  // キャプションにaltを表示
}

function closeImageModal() {
    var modal = document.getElementById("myModalImage");
    modal.style.display = "none";  // モーダルを非表示
}


// プラスボタンが押された時だけモーダルを開く
document.querySelector(".fixed-add-btn").addEventListener("click", openQuoteModal);

// モーダルを開く関数
function openQuoteModal() {
    var modal = document.getElementById("quoteModal");
    var modalBackground = document.getElementById("modalBackground");
    modal.style.display = "block";
    modalBackground.style.display = "block";
}

// モーダルを閉じる関数
function closeQuoteModal() {
    var modal = document.getElementById("quoteModal");
    var modalBackground = document.getElementById("modalBackground");
    modal.style.display = "none";
    modalBackground.style.display = "none";
}

// モーダル外をクリックして閉じる処理
window.onclick = function(event) {
    var modal = document.getElementById("quoteModal");
    var modalBackground = document.getElementById("modalBackground");
    if (event.target == modalBackground) {
        modal.style.display = "none";
        modalBackground.style.display = "none";
    }
}


// 編集ボタンのクリック時にイベント伝播を止める
document.querySelectorAll('.edit-link').forEach(function(editLink) {
    editLink.addEventListener('click', function(event) {
        event.stopPropagation();  // イベント伝播を停止
    });
});

// 名言カードをクリックすると詳細ページに移動する
document.querySelectorAll('.quote-card').forEach(function(card) {
    card.addEventListener('click', function() {
        var url = card.querySelector('.quote-card-link').href;
        window.location.href = url;  // カード全体をリンクとして機能させる
    });
});
