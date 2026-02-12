document.addEventListener("DOMContentLoaded", () => {
  const nameInput = document.getElementById("name");
  const emailInput = document.getElementById("email");
  const passwordInput = document.getElementById("password");
  const confirmInput = document.getElementById("passwordConfirm"); // ← 正しいIDに
  const btn = document.getElementById("signupBtn");

  const bar = document.getElementById("pwBar");
  const label = document.getElementById("pwLabel");

  const passwordError = document.getElementById("passwordError");
  const confirmError = document.getElementById("confirmError");
  const emailError = document.getElementById("emailError");

  // 必須要素が無ければ何もしない
  if (!passwordInput || !confirmInput || !btn || !bar || !label) return;

  function updateStrengthUI(score, hasPassword) {
    if (!hasPassword) {
      bar.style.width = "0%";
      bar.style.backgroundColor = "transparent";
      label.textContent = "パスワード強度：-";
      return;
    }

    if (score <= 1) {
      bar.style.width = "33%";
      bar.style.backgroundColor = "#e74c3c";
      label.textContent = "パスワード強度：弱い";
    } else if (score === 2) {
      bar.style.width = "66%";
      bar.style.backgroundColor = "#f1c40f";
      label.textContent = "パスワード強度：普通";
    } else {
      bar.style.width = "100%";
      bar.style.backgroundColor = "#2ecc71";
      label.textContent = "パスワード強度：強い";
    }
  }

  function validate() {
    const name = nameInput ? nameInput.value.trim() : "";
    const email = emailInput ? emailInput.value.trim() : "";
    const password = passwordInput.value || "";
    const confirm = confirmInput.value || "";

    // --- スコア算出（zxcvbnが無い場合は0扱い） ---
    const score =
      password && typeof zxcvbn === "function" ? zxcvbn(password).score : 0;

    // --- 強度バー更新 ---
    updateStrengthUI(score, password.length > 0);

    // --- リアルタイムアラート ---
    // パスワードが弱い（入力がある時だけ出す）
    if (passwordError) {
      if (password && score < 3) {
        passwordError.textContent = "パスワードが弱いです（強にしてください）";
        passwordError.style.display = "block";
      } else {
        passwordError.textContent = "";
        passwordError.style.display = "none";
      }
    }

    // --- メール形式チェック ---
    if (emailError) {
      const email = emailInput.value.trim();

      // 空ならエラーは出さない
      if (email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

        if (!emailRegex.test(email)) {
          emailError.textContent = "正しいメールアドレス形式で入力してください";
          emailError.style.display = "block";
          validEmail = false;
        } else {
          emailError.textContent = "";
          emailError.style.display = "none";
          validEmail = true;
        }
      } else {
        emailError.textContent = "";
        emailError.style.display = "none";
        validEmail = false;
      }
    }

    // 確認用と不一致（確認用に入力がある時だけ出す）
    if (confirmError) {
      if (confirm && password !== confirm) {
        confirmError.textContent = "パスワードが一致していません";
        confirmError.style.display = "block";
      } else {
        confirmError.textContent = "";
        confirmError.style.display = "none";
      }
    }

    // --- ボタン有効条件 ---
    const filled =
      name !== "" && email !== "" && password !== "" && confirm !== "";
    const strong = password !== "" && score >= 3;
    const match = confirm !== "" && password === confirm;

    btn.disabled = !(filled && strong && match);
  }

  // 入力が変わるたびにまとめて更新
  [nameInput, emailInput, passwordInput, confirmInput].forEach((el) => {
    if (el) el.addEventListener("input", validate);
  });

  // 初期状態反映
  validate();
});
