document.getElementById('add-sibling-btn').addEventListener('click', function() {
    // 子ども情報入力フォームのコンテナを取得
    var container = document.getElementById('child-form-container');

    // 新しいフォームを作成
    var newForm = document.createElement('div');
    newForm.classList.add('child-form');
    newForm.innerHTML = `
        <div class="form-group">
            <label for="nickname">ニックネーム:</label>
            <input type="text" name="nickname" required>
        </div>
        <div class="form-group">
            <label for="birthdate">生年月日:</label>
            <input type="date" name="birthdate" value="${new Date().toISOString().slice(0, 10)}" required>
        </div>
    `;

    // コンテナに新しいフォームを追加
    container.appendChild(newForm);
});

