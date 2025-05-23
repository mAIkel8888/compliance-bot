const sections = {
    past_inventory: { title: "過去の棚卸し", questions: ["子どもの頃、夢中になったことは何でしたか？今でもそれは大切ですか？", "「あのとき、嬉しかった」と今でも思い出せる瞬間は？", "大人になってから、自然に涙が出た出来事は？", "「自分らしかった」と言える過去のエピソードはどんなものですか？", "あのときの選択が、もし逆だったらどうなっていたと思いますか？"] },
    emotion_manual: { title: "今の感情の取扱説明書", questions: ["最近感じた「小さな怒り」には、どんな意味がありそうですか？", "自分が安心する瞬間は、どんな状況ですか？", "「他人の言葉」で傷ついた経験を、今どう理解していますか？", "今、あなたの心がいちばん求めているものは？", "もし1日誰にも会わなくていいとしたら、何をして過ごしたいですか？"] },
    values_layers: { title: "価値観の地層を掘る", questions: ["「この考え方は譲れない」と感じるものは何ですか？", "どんな言葉を聞くと、あなたは心が軽くなりますか？", "あなたが「大切にされている」と感じるときは、どんなときですか？", "理想の社会とは、どんな状態だと思いますか？", "どんな人を見ると「この人好きだな」と思いますか？"] },
    ideal_life: { title: "理想の生活と人間関係", questions: ["毎日1時間だけ、自由に使えるとしたら何に使いますか？", "一緒にいて安心できる人って、どんな人ですか？", "こんな習慣があれば、自分はもっと幸せになれると思うことは？", "あなたが「無理をせず自然体」でいられるのはどんな空間ですか？", "誰にも否定されずに話せるなら、今何を話したいですか？"] },
    occupational_dna: { title: "あなたの職業的DNA", questions: ["「自分が役に立った」と感じた瞬間は、どんなときですか？", "お金が発生しなくても、続けたいと思える活動はありますか？", "「人を育てる」中で、自分が得た学びは何でしたか？", "過去の仕事経験で、今も誇りに思えることは？", "「この仕事は、向いてなかったな」と思う理由は何でしたか？"] },
    future_choices: { title: "明日をつくる選択", questions: ["もし今すぐ新しい一歩を踏み出すとしたら、何をしますか？", "「いつかやろう」と思っていることの中で、一番小さく始められるものは？", "理想の1日は、どんな流れで始まり、終わりますか？", "自分を信じるために、まず何を手放すべきですか？", "未来の自分が、今の自分にひとこと言うとしたら、なんて言うと思いますか？"] }
};

let currentSectionId = "past_inventory"; // Default to the first section
let currentQuestionIndex = 0;
let allQuestionsFlat = []; // To be populated once

function populateAllQuestionsFlat() {
    allQuestionsFlat = []; // Reset if called multiple times, though intended once
    for (const sId in sections) {
        if (sections.hasOwnProperty(sId)) {
            sections[sId].questions.forEach((qText, qIdx) => {
                allQuestionsFlat.push({ sectionId: sId, questionIndex: qIdx, text: qText });
            });
        }
    }
}

function getQuestionOfTheDay() {
    if (allQuestionsFlat.length === 0) return null;

    const today = new Date().toDateString(); // Use toDateString for day-level comparison
    const lastShownDate = localStorage.getItem('qotd_last_shown_date');
    let globalIndex = parseInt(localStorage.getItem('qotd_last_global_index'), 10);

    if (isNaN(globalIndex) || globalIndex < 0 || globalIndex >= allQuestionsFlat.length) { // Ensure index is valid
        globalIndex = -1; // Start before first question or reset if invalid
    }

    if (lastShownDate !== today) {
        globalIndex++;
        if (globalIndex >= allQuestionsFlat.length) {
            globalIndex = 0; // Loop back
        }
        localStorage.setItem('qotd_last_global_index', globalIndex.toString());
        localStorage.setItem('qotd_last_shown_date', today);
    }
    // If it is the same day, or after updating index for new day, return the question
    // Ensure globalIndex is valid before accessing allQuestionsFlat
    if (globalIndex < 0 || globalIndex >= allQuestionsFlat.length) { // Should not happen if logic above is correct
      return allQuestionsFlat.length > 0 ? allQuestionsFlat[0] : null; // Default to first question if error
    }
    return allQuestionsFlat[globalIndex];
}

function displayQuestionOfTheDay() {
    const qotdData = getQuestionOfTheDay();
    const qotdContainer = document.getElementById('qotd-container'); 

    if (qotdData && qotdContainer) {
        const qotdTextElement = document.getElementById('qotd-text');
        const qotdAnswerButton = document.getElementById('qotd-answer-button');

        qotdTextElement.textContent = qotdData.text;
        qotdContainer.style.display = 'block'; // Make it visible

        qotdAnswerButton.onclick = () => { 
            currentSectionId = qotdData.sectionId;
            currentQuestionIndex = qotdData.questionIndex;
            // Ensure the main display function is called to show this question
            displayQuestion(); 
            qotdContainer.style.display = 'none'; // Optionally hide QOTD after click
        };
    } else if (qotdContainer) {
        // If no QOTD data (e.g., no questions at all), hide the container
        qotdContainer.style.display = 'none';
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const sectionTitleElement = document.getElementById('current-section-title');
    const questionDisplayElement = document.getElementById('question-display-area');
    const navigationLinks = document.querySelectorAll('#section-navigation a');
    const prevButton = document.getElementById('prev-question');
    const nextButton = document.getElementById('next-question');
    const questionNavigationButtons = document.getElementById('navigation-buttons');

    // References to dynamically created elements, will be reassigned in displayQuestion
    let questionTextElement, answerInputElement, saveAnswerButton;

    function createQuestionUI() {
        questionDisplayElement.innerHTML = ''; // Clear previous content (e.g., history)

        questionTextElement = document.createElement('p');
        
        answerInputElement = document.createElement('textarea');
        answerInputElement.id = 'answer-input';
        answerInputElement.rows = 5;
        answerInputElement.placeholder = 'ここに回答を入力してください...';
        answerInputElement.style.width = '90%';
        answerInputElement.style.marginTop = '10px';

        saveAnswerButton = document.createElement('button');
        saveAnswerButton.id = 'save-answer';
        saveAnswerButton.textContent = '回答を保存';
        saveAnswerButton.style.display = 'block';
        saveAnswerButton.style.marginTop = '10px';
        saveAnswerButton.addEventListener('click', () => {
            const answerText = answerInputElement.value.trim();
            const key = `answer_${currentSectionId}_${currentQuestionIndex}`;
            localStorage.setItem(key, answerText);
            alert('回答を保存しました！');
        });

        questionDisplayElement.appendChild(questionTextElement);
        questionDisplayElement.appendChild(answerInputElement);
        questionDisplayElement.appendChild(saveAnswerButton);

        const shareButton = document.createElement('button');
        shareButton.id = 'share-button';
        shareButton.textContent = 'この問答をコピー';
        // Basic styling, can be enhanced in CSS
        shareButton.style.marginLeft = '10px'; 
        shareButton.style.display = 'inline-block'; // To be on the same line as save if possible
        
        shareButton.addEventListener('click', () => {
            const questionText = sections[currentSectionId].questions[currentQuestionIndex];
            // Ensure answerInputElement is the current, valid one from createQuestionUI
            const answerText = answerInputElement.value.trim(); 

            let shareText = `【こころの地図帳より】
Q: ${questionText}`;
            if (answerText) {
                shareText += `
A: ${answerText}`;
            } else {
                shareText += `
A: (まだ回答していません)`;
            }
            shareText += "\n\n#こころの地図帳 #自己分析";

            if (navigator.clipboard && navigator.clipboard.writeText) {
                navigator.clipboard.writeText(shareText)
                    .then(() => {
                        alert('クリップボードにコピーしました！');
                    })
                    .catch(err => {
                        console.error('Clipboard copy failed:', err);
                        alert('コピーに失敗しました。');
                    });
            } else {
                alert('クリップボード機能が利用できません。手動でコピーしてください。');
                console.warn('navigator.clipboard.writeText is not available.');
            }
        });
        // Append shareButton next to saveAnswerButton.
        // Since saveAnswerButton is block, shareButton might appear below.
        // A container div for buttons would be better for layout, or adjust display styles.
        // For now, just append it. If saveAnswerButton.style.display is 'block', this will be on new line.
        // Let's ensure saveAnswerButton is also inline-block for them to be side-by-side.
        saveAnswerButton.style.display = 'inline-block'; 
        questionDisplayElement.appendChild(shareButton);
    }

    function loadAnswer() {
        // Ensure answerInputElement is valid (i.e., question UI is active)
        if (!answerInputElement) return; 
        const key = `answer_${currentSectionId}_${currentQuestionIndex}`;
        const savedAnswer = localStorage.getItem(key);
        if (savedAnswer !== null) {
            answerInputElement.value = savedAnswer;
        } else {
            answerInputElement.value = '';
        }
    }

    function displayQuestion() {
        createQuestionUI(); // Rebuilds the question UI elements
        questionNavigationButtons.style.display = 'block'; // Or 'flex' etc.

        if (sections[currentSectionId]) {
            const section = sections[currentSectionId];
            sectionTitleElement.textContent = section.title;
            if (section.questions.length > 0 && currentQuestionIndex >= 0 && currentQuestionIndex < section.questions.length) {
                questionTextElement.textContent = section.questions[currentQuestionIndex];
                prevButton.disabled = currentQuestionIndex === 0;
                nextButton.disabled = currentQuestionIndex === section.questions.length - 1;
                answerInputElement.style.display = 'block';
                saveAnswerButton.style.display = 'block';
            } else if (section.questions.length === 0) {
                questionTextElement.textContent = "このセクションにはまだ質問がありません。";
                prevButton.disabled = true;
                nextButton.disabled = true;
                answerInputElement.style.display = 'none';
                saveAnswerButton.style.display = 'none';
            } else { // Index out of bounds (e.g. after last question)
                questionTextElement.textContent = "このセクションの質問は以上です。";
                prevButton.disabled = currentQuestionIndex <= 0;
                nextButton.disabled = true; // Always true if past the last question
                answerInputElement.style.display = 'none';
                saveAnswerButton.style.display = 'none';
            }
        } else { // Should not happen if navigation is correct
            sectionTitleElement.textContent = "セクションが見つかりません";
            questionTextElement.textContent = "選択されたセクションのデータが見つかりません。";
            prevButton.disabled = true;
            nextButton.disabled = true;
            answerInputElement.style.display = 'none';
            saveAnswerButton.style.display = 'none';
        }
        loadAnswer();
    }

    function displayAnswerHistory() {
        sectionTitleElement.textContent = "回答履歴一覧";
        questionDisplayElement.innerHTML = ''; // Clear question UI
        questionNavigationButtons.style.display = 'none'; // Hide prev/next buttons

        let historyHtml = "";
        let answersFound = false;

        for (const sId in sections) {
            if (sections.hasOwnProperty(sId)) {
                const section = sections[sId];
                historyHtml += `<h3>${section.title}</h3>`;
                let sectionHasAnswers = false;
                section.questions.forEach((questionText, qIndex) => {
                    const key = `answer_${sId}_${qIndex}`;
                    const savedAnswer = localStorage.getItem(key);
                    if (savedAnswer !== null && savedAnswer.trim() !== "") {
                        historyHtml += `<div class="history-item">
                                          <p class="history-question"><strong>Q:</strong> ${questionText}</p>
                                          <p class="history-answer"><strong>A:</strong> ${savedAnswer.replace(/\n/g, '<br>')}</p>
                                       </div>`;
                        answersFound = true;
                        sectionHasAnswers = true;
                    } else {
                         historyHtml += `<div class="history-item">
                                          <p class="history-question"><strong>Q:</strong> ${questionText}</p>
                                          <p class="history-answer"><strong>A:</strong> (未回答)</p>
                                       </div>`;
                    }
                });
                 if (!sectionHasAnswers && section.questions.length > 0){
                     // historyHtml += "<p style='margin-left:1em; font-style:italic;'>(このセクションの回答はありません)</p>"; // Optional per-section message
                 }
            }
        }

        if (!answersFound) {
            historyHtml = "<p>まだ保存された回答はありません。</p>";
        }
        
        questionDisplayElement.innerHTML = historyHtml;
    }

    navigationLinks.forEach(link => {
        link.addEventListener('click', (event) => {
            event.preventDefault();
            const sectionId = link.dataset.sectionId;
            if (sectionId === "answer_history") {
                currentSectionId = "answer_history"; 
                displayAnswerHistory();
            } else if (sectionId === "personality_diagnosis") {
                currentSectionId = "personality_diagnosis"; // Optional: if needed for state
                displayPersonalityDiagnosisPlaceholder();
            } else if (sections[sectionId]) {
                currentSectionId = sectionId;
                currentQuestionIndex = 0;
                displayQuestion();
            }
        });
    });

    function displayPersonalityDiagnosisPlaceholder() {
        sectionTitleElement.textContent = "性格傾向診断"; // Update main title
        
        if (questionNavigationButtons) questionNavigationButtons.style.display = 'none';

        let placeholderHtml = "";
        placeholderHtml += "<h2>この機能について</h2>";
        placeholderHtml += "<p>この「性格傾向診断」機能は現在開発中です。</p>";
        placeholderHtml += "<p>将来的には、あなたの回答に基づいて、あなたの内面をより深く理解するためのお手伝いをすることを目指しています。MBTIやビッグファイブのような分析とは異なりますが、あなた自身の言葉からパターンを見つけ出し、自己再発見を促すようなヒントを提供できればと考えています。</p>";
        
        let answeredQuestionsCount = 0;
        const totalQuestions = allQuestionsFlat.length > 0 ? allQuestionsFlat.length : Object.values(sections).reduce((acc, section) => acc + section.questions.length, 0);

        if (allQuestionsFlat && allQuestionsFlat.length > 0) {
            allQuestionsFlat.forEach(q_item => {
                const key = `answer_${q_item.sectionId}_${q_item.questionIndex}`;
                const savedAnswer = localStorage.getItem(key);
                if (savedAnswer !== null && savedAnswer.trim() !== "") {
                    answeredQuestionsCount++;
                }
            });
        } else { 
            for (const sId_loop in sections) { // Renamed sId to sId_loop to avoid conflict if any
                if (sections.hasOwnProperty(sId_loop)) {
                    sections[sId_loop].questions.forEach((_, qIndex_loop) => { // Renamed qIndex to qIndex_loop
                        const key = `answer_${sId_loop}_${qIndex_loop}`;
                        const savedAnswer = localStorage.getItem(key);
                        if (savedAnswer !== null && savedAnswer.trim() !== "") {
                            answeredQuestionsCount++;
                        }
                    });
                }
            }
        }
        
        placeholderHtml += `<p style="margin-top: 20px;"><strong>進捗状況：</strong> あなたは現在、全 ${totalQuestions} 問中 ${answeredQuestionsCount} 問に回答しています。</p>`;
        if (answeredQuestionsCount > 0) {
            placeholderHtml += "<p>素晴らしいスタートです！多くの質問に答えるほど、より豊かな自己理解に繋がるかもしれません。</p>";
        } else {
            placeholderHtml += "<p>まずはいくつかの質問に答えてみましょう。そこから何が見えてくるでしょうか。</p>";
        }

        placeholderHtml += "<p style='margin-top: 30px; font-weight: bold;'>どうぞお楽しみに！</p>";
        
        questionDisplayElement.innerHTML = placeholderHtml;
    }

    prevButton.addEventListener('click', () => {
        if (currentQuestionIndex > 0) {
            currentQuestionIndex--;
            displayQuestion(); // displayQuestion will recreate UI and load the correct state
        }
    });

    nextButton.addEventListener('click', () => {
        if (sections[currentSectionId] && currentQuestionIndex < sections[currentSectionId].questions.length - 1) {
            currentQuestionIndex++;
            displayQuestion(); // displayQuestion will recreate UI and load the correct state
        }
    });

    // Initial display (default section)
    populateAllQuestionsFlat(); // Populate the flat list of questions
    displayQuestionOfTheDay();   // Display QOTD logic

    // The rest of the DOMContentLoaded, including event listeners and initial main display call
    if (sections[currentSectionId] && currentSectionId !== "answer_history") { 
        // If currentSectionId was changed by QOTD button, displayQuestion was already called by its onclick.
        // This check ensures we don't call displayQuestion() again if QOTD was interacted with.
        // However, the qotdAnswerButton.onclick handles calling displayQuestion.
        // The main concern is the very first load before any interaction.
        // If QOTD is displayed, and user *doesn't* click its button, the default section should load.
        // If currentSectionId is NOT changed by QOTD (i.e., user hasn't clicked QOTD button yet),
        // then we load the default section.
        const qotdContainer = document.getElementById('qotd-container');
        let qotdClicked = false; // A simplistic way to check; better if onclick sets a flag or if currentSectionId is compared to initial default
        
        // A more direct way: if QOTD button was clicked, currentSectionId and currentQuestionIndex are already set
        // and displayQuestion() was called. So, we only call displayQuestion() here if it's the initial page load
        // without QOTD interaction leading to a displayQuestion() call.
        // The current logic: displayQuestion() always gets called for the default section unless QOTD interaction changed section.
        // This is generally fine. QOTD is an overlay.

        // Let's simplify: QOTD is displayed. The main area loads its default.
        // If QOTD answer button is clicked, main area re-renders.
        displayQuestion();

    } else if (currentSectionId === "answer_history") {
        // If default is somehow answer_history, or set by other means (not QOTD)
        displayAnswerHistory();
    } else {
        // Fallback if default currentSectionId is somehow invalid
        const firstSectionId = Object.keys(sections)[0];
        if (firstSectionId) {
            currentSectionId = firstSectionId;
            currentQuestionIndex = 0;
            displayQuestion();
        } else {
            sectionTitleElement.textContent = "エラー";
            questionDisplayElement.innerHTML = "<p>セクションデータが見つかりません。</p>";
            if(questionNavigationButtons) questionNavigationButtons.style.display = 'none';
        }
    }
});
