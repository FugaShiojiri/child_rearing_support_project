/**
 * ひだまりこそだち — Phase 1 インタビュー Form 自動生成スクリプト
 *
 * 出典: docs/interview_form_v1.md（status: ceo_approved / 2026-05-15 CEOレビュー完了）
 *
 * ===== 使い方（CEO本人が1回だけ実施・約5〜10分）=====
 * 1. https://script.google.com を hidamarikosodachi@gmail.com で開く
 * 2. 「新しいプロジェクト」→ エディタの中身を全消し → 本ファイルの内容を全て貼り付け
 * 3. 上部の関数選択で createHidamariInterviewForm を選び「実行」
 * 4. 初回は権限承認ダイアログ → アカウントを選び「許可」（同一Googleアカウント内のみ・無料）
 * 5. 実行ログ（表示 > ログ）に「編集URL」と「回答用URL」が出る。編集URLでCEO最終目視 → 回答用URLを配布
 *
 * ※ Apps Script は取得済み Gmail アカウントに標準付属。GCP・有料SaaS不要。
 * ※ 再実行すると毎回「新しいFormが1つ」作られる。作り直したい時だけ再実行する。
 */

// ===== CONFIG（必要なら true/false を変更。既定は回答離脱を最小化する設定）=====
var CONFIG = {
  // FORM_ID を指定すると「既存フォームを同じURLのまま中身を作り直す」（孤児フォームを作らない・配布URL不変）。
  // 空文字 '' にすると毎回「新規フォーム」を作成する。
  // 既存フォーム: https://docs.google.com/forms/d/125kDpFxPQZ0Ld8HaPFvdGAX6p3CKxc3BL89vh2tRwhE/edit
  FORM_ID: '125kDpFxPQZ0Ld8HaPFvdGAX6p3CKxc3BL89vh2tRwhE',
  // note が公開済みなら note の URL を入れる（空なら本文にリンクを出さずテキストのみ）。
  NOTE_URL: 'https://note.com/hidamari_sodachi/n/n0e6db37bd948',
  // ※ REQUIRE_LOGIN / LIMIT_ONE_RESPONSE は Google Workspace（独自ドメイン）専用。
  //   個人Gmail（@gmail.com）では未対応なので false のまま使う（true にしても自動スキップされる）。
  REQUIRE_LOGIN: false,          // Workspace限定: Googleログイン必須
  LIMIT_ONE_RESPONSE: false,     // Workspace限定: 1人1回（REQUIRE_LOGIN=true が前提）
  PROGRESS_BAR: true,
  SHUFFLE: false
};

function createHidamariInterviewForm() {
  var FORM_TITLE = '子育てと『学びの考え方』についての小さなアンケート 〜ひだまりこそだち〜';
  var form;
  if (CONFIG.FORM_ID) {
    // 既存フォームを再利用（URL不変・孤児フォームを作らない）。中身を全削除して作り直す。
    form = FormApp.openById(CONFIG.FORM_ID);

    // ★ 先に分岐ナビゲーションを解除する。
    //   Q1.1 の選択肢が対象外ページ(PageBreak)を指したまま PageBreak を削除すると
    //   「Invalid data updating form」になるため、削除前に必ず参照を断ち切る。
    var cur = form.getItems();
    for (var a = 0; a < cur.length; a++) {
      var itA = cur[a];
      if (itA.getType() === FormApp.ItemType.MULTIPLE_CHOICE) {
        try {
          var mcA = itA.asMultipleChoiceItem();
          var vals = mcA.getChoices().map(function (c) { return c.getValue(); });
          if (vals.length > 0) {
            mcA.setChoices(vals.map(function (v) { return mcA.createChoice(v); }));
          }
        } catch (e1) { Logger.log('[navクリア スキップ MC] ' + e1.message); }
      } else if (itA.getType() === FormApp.ItemType.PAGE_BREAK) {
        try {
          itA.asPageBreakItem().setGoToPage(FormApp.PageNavigationType.CONTINUE);
        } catch (e2) { Logger.log('[navクリア スキップ PB] ' + e2.message); }
      }
    }

    // ナビゲーション解除後に末尾から削除
    var existing = form.getItems();
    for (var k = existing.length - 1; k >= 0; k--) {
      form.deleteItem(existing[k]);
    }
    form.setTitle(FORM_TITLE);
    Logger.log('[再利用] 既存フォームの中身を作り直します: ' + CONFIG.FORM_ID);
  } else {
    form = FormApp.create(FORM_TITLE);
    Logger.log('[新規] フォームを新規作成しました');
  }

  form.setDescription(
    'はじめまして。「ひだまりこそだち」は、子育ての「学びや関わり方の考え方」について、' +
    'いろいろな見方をやさしく並べて、その方にあったものをそっとお渡しできないか、を考えている小さな試みです。\n' +
    'このアンケートは、これからの形を決めるための声集めです（5分ほど・任意項目が中心です）。' +
    '「正解はひとつではない」という前提で読んでいただけたらうれしいです。'
  );

  // 個人Gmailアカウントでは一部メソッドが Workspace 専用で未対応のため、安全に適用する
  function safe(label, fn) {
    try { fn(); } catch (e) { Logger.log('[スキップ] ' + label + ' は当アカウントで未対応: ' + e.message); }
  }

  safe('setProgressBar', function () { form.setProgressBar(CONFIG.PROGRESS_BAR); });
  safe('setCollectEmail', function () { form.setCollectEmail(false); }); // メールは Q8.2 で任意取得
  safe('setShuffleQuestions', function () { form.setShuffleQuestions(CONFIG.SHUFFLE); });
  safe('setShowLinkToRespondAgain', function () { form.setShowLinkToRespondAgain(false); });

  // ↓ setRequireLogin / setLimitOneResponsePerUser は Google Workspace（独自ドメイン）専用。
  //   個人Gmailでは「This operation is not supported」になるため、CONFIG が true のときだけ試行する。
  //   既定（false）では呼ばない＝個人Gmailで重複抑制は Form 機能では行わず、配布動線側で管理する。
  if (CONFIG.REQUIRE_LOGIN) {
    safe('setRequireLogin', function () { form.setRequireLogin(true); });
    if (CONFIG.LIMIT_ONE_RESPONSE) {
      safe('setLimitOneResponsePerUser', function () { form.setLimitOneResponsePerUser(true); });
    }
  }

  var CONT = FormApp.PageNavigationType.CONTINUE;
  var SUBMIT = FormApp.PageNavigationType.SUBMIT;

  // ========== S1: スクリーニング（フォーム先頭ページ）==========
  form.addSectionHeaderItem()
    .setTitle('S1. はじめに')
    .setHelpText('いちばん下のお子さまについて教えてください。');

  var q11 = form.addMultipleChoiceItem();
  q11.setTitle('Q1.1 いちばん下のお子さまの年齢を教えてください').setRequired(true);

  var q12 = form.addMultipleChoiceItem();
  q12.setTitle('Q1.2 回答者の立場（任意）').setRequired(false)
     .setChoiceValues(['母親', '父親', '祖父母', 'その他養育者']);

  var q13 = form.addMultipleChoiceItem();
  q13.setTitle('Q1.3 お子さまの人数（任意）').setRequired(false)
     .setChoiceValues(['1人', '2人', '3人以上']);

  // ========== S2 ==========
  var pbS2 = form.addPageBreakItem().setTitle('S2. 子育ての現状・困りごと');

  var S2_CONCERNS = [
    '生活リズム・食事・睡眠など毎日の運用',
    '発達や成長のペースが気になる',
    '関わり方・声かけの仕方に迷う',
    'しつけ・約束・気持ちの切り替え',
    '学び・遊び・就学準備をどうするか',
    '相談相手が少ない・ひとりで抱えがち',
    '自分の時間が持てない',
    '教育や情報が多すぎて選べない',
    'その他'
  ];

  var q21 = form.addCheckboxItem();
  q21.setTitle('Q2.1 日々の子育てで、いま気になっていること（あてはまるものを最大3つまで・任意）')
     .setRequired(false)
     .setChoiceValues(S2_CONCERNS);
  safe('Q2.1 最大3つ検証', function () {
    q21.setValidation(FormApp.createCheckboxValidation().requireSelectAtMost(3).build());
  });

  var q21b = form.addMultipleChoiceItem();
  q21b.setTitle('Q2.1b その中で「いちばん解決したい」もの1つ（任意）')
      .setHelpText('複数選んでくださった方は、その中でいちばん手をつけたいものを1つだけ。')
      .setRequired(false)
      .setChoiceValues(S2_CONCERNS);

  var q22 = form.addMultipleChoiceItem();
  q22.setTitle('Q2.2 「いろいろな育児情報を見て、結局どれを信じればいいか迷う」ことはありますか（任意）')
     .setRequired(false)
     .setChoiceValues(['1 ほぼない', '2 あまりない', '3 どちらとも', '4 ときどきある', '5 よくある']);

  var q23 = form.addCheckboxItem();
  q23.setTitle('Q2.3 過去1年で「やめた／続かなかった」育児系サービス・教材があれば（複数可・任意）')
     .setRequired(false)
     .setChoiceValues([
       'こどもちゃれんじ', 'スマイルゼミ', 'ポピー', 'Z会幼児', 'ワンダーボックス',
       '知育玩具サブスク', '育児系メルマガ・note', 'SNS・YouTube の育児情報',
       '相談系サービス', '使ったことがない', 'その他'
     ]);

  var q24 = form.addParagraphTextItem();
  q24.setTitle('Q2.4 上の選択肢では言い表せない「子育てで、いま、いちばんモヤモヤすること」があれば、ふだんの言葉で（任意・1〜2行）')
     .setHelpText('うまく言葉にならなくても大丈夫です。空欄でも構いません。')
     .setRequired(false);

  // ========== S3 ==========
  var pbS3 = form.addPageBreakItem().setTitle('S3. 子育ての考え方の「届け方」について');

  var q31 = form.addGridItem();
  q31.setTitle('Q3.1 次のような「子育ての考え方の届け方」、それぞれどのくらい魅力を感じますか（任意）')
     .setRows([
       'a. 短い読み物（note などの記事を、無理なく読めるペースで）',
       'b. まとまった資料（年代別の「関わり方ガイド」PDF を手元に置ける）',
       'c. 提案の仕組み（いくつかの質問に答えると、自分に合いそうな考え方を提案してくれる）',
       'd. オフラインの集まり（近くで、ゆるく話せる場）'
     ])
     .setColumns(['1 魅力を感じない', '2', '3', '4', '5 とても魅力を感じる']);

  var q32 = form.addMultipleChoiceItem();
  q32.setTitle('Q3.2 子育て情報について、どちらの感覚に近いですか（任意）')
     .setRequired(false)
     .setChoiceValues([
       '1 やり方を1つにしぼって教えてほしい',
       '2',
       '3 どちらとも',
       '4',
       '5 いろいろな考え方を並べて、自分で選びたい'
     ]);

  var q33 = form.addMultipleChoiceItem();
  q33.setTitle('Q3.3 「研究・専門家の知見にもとづいている」ことは、あなたにとってどのくらい大事ですか（任意）')
     .setHelpText('ひだまりこそだち は、いろいろな教育・発達の考え方を整理した上で内容をつくっています。特定の流派を断言することはしません。')
     .setRequired(false)
     .setChoiceValues(['1 あまり気にしない', '2', '3 どちらとも', '4', '5 とても大事']);

  // ========== S4: ガイドPDF への反応（親向けのみ・実物提示なし）==========
  var pbS4 = form.addPageBreakItem().setTitle('S4. 「関わり方ガイド（PDF）」について');
  form.addSectionHeaderItem()
    .setTitle('【ご紹介する資料の例】')
    .setHelpText(
      '「1歳から2歳になる子へ ― 関わり方ガイド」というPDF資料を用意しています。' +
      'アタッチメント／モンテッソーリ／ピクラー／アドラー／NVC など、いくつかの立場から' +
      '「同じ場面」をどう見るかを並べた、読み物に近い手引きです（数十ページ程度）。' +
      '「こうしてください」ではなく「こんな選択肢もあります」という書き方をしています。'
    );

  var q41 = form.addMultipleChoiceItem();
  q41.setTitle('Q4.1 このような「年代別の関わり方ガイド（PDF）」、手元にあったら読みたいと思いますか（任意）')
     .setRequired(false)
     .setChoiceValues(['1 思わない', '2', '3 どちらとも', '4', '5 とても読みたい']);

  var q42 = form.addMultipleChoiceItem();
  q42.setTitle('Q4.2 このガイドが届くなら、どれが近いですか（任意）')
     .setRequired(false)
     .setChoiceValues([
       '無料なら読みたい',
       '数百円までなら払ってもよい（〜¥500目安）',
       '千円前後までなら払ってもよい（〜¥1,000目安）',
       '内容次第でそれ以上も',
       '有料なら読まない'
     ]);

  var q43 = form.addMultipleChoiceItem();
  q43.setTitle('Q4.3 年代別のシリーズ（例: 0〜1歳 / 1〜2歳 / 2〜3歳 …）として続くなら、期待しますか（任意）')
     .setRequired(false)
     .setChoiceValues(['1 期待しない', '2', '3 どちらとも', '4', '5 とても期待する']);

  var q44 = form.addCheckboxItem();
  q44.setTitle('Q4.4 あなたが「いま欲しい」と思う年代があれば（複数可・任意）')
     .setRequired(false)
     .setChoiceValues(['0〜1歳', '1〜2歳', '2〜3歳', '3〜4歳', '5〜6歳', '年代より「テーマ別」がいい', '特にない']);

  // ========== S5: マッチャー受容性 ==========
  var pbS5 = form.addPageBreakItem().setTitle('S5. 「自分に合う考え方を提案する仕組み」について');
  form.addSectionHeaderItem()
    .setTitle('【考えている仕組みの例】')
    .setHelpText(
      'いくつかの質問に答えると、「あなたの今の関わり方の傾向」をやさしく言葉にして、' +
      'それに近い考え方・関わり方の選択肢を、性格タイプの読み物のような感覚で並べて見られる ── ' +
      'そんな仕組みを考えています。\n' +
      'どの関わり方にもよさがあります。「これが正しい」と決めつけたり、タイプに固定したりはしません。' +
      '今の傾向のスナップショット、くらいの気持ちで使えるものを目指しています。'
    );

  var q51 = form.addMultipleChoiceItem();
  q51.setTitle('Q5.1 このような「自分に合いそうな子育ての考え方を提案してくれる仕組み」、使ってみたいと思いますか（任意）')
     .setRequired(false)
     .setChoiceValues(['1 思わない', '2', '3 どちらとも', '4', '5 とても使ってみたい']);

  var q52 = form.addMultipleChoiceItem();
  q52.setTitle('Q5.2 「子育ての考え方は人それぞれで、正解はひとつではない」という考え方に、どのくらい共感しますか（任意）')
     .setRequired(false)
     .setChoiceValues(['1 共感しない', '2', '3 どちらとも', '4', '5 とても共感する']);

  var q53 = form.addMultipleChoiceItem();
  q53.setTitle('Q5.3 こうした仕組み、どんな条件なら使ってみたいですか（任意）')
     .setRequired(false)
     .setChoiceValues([
       '無料なら使ってみたい',
       '無料で試して、結果が役立てば有料の続きも検討する',
       '数百円程度なら最初から有料でもよい',
       '千円前後でも内容次第で',
       'こうした仕組み自体に興味がない'
     ]);

  var q54 = form.addMultipleChoiceItem();
  q54.setTitle('Q5.4 これまでに、似たもの（性格診断・育児タイプ診断・親タイプ診断など）を使ったことはありますか（任意）')
     .setRequired(false)
     .setChoiceValues(['ある（役に立った）', 'ある（あまり役に立たなかった）', 'ない', '覚えていない']);

  var q54t = form.addParagraphTextItem();
  q54t.setTitle('Q5.4（つづき）もしあれば、サービス名や「良かった点・物足りなかった点」を一言（任意）')
      .setRequired(false);

  var q55 = form.addCheckboxItem();
  q55.setTitle('Q5.5 結果として、どんな形がうれしいですか（複数可・任意）')
     .setRequired(false)
     .setChoiceValues([
       '自分の傾向の言葉での説明',
       '合いそうな関わり方の具体例',
       '合いそうな本や記事の紹介',
       '「やってみると良いこと」を1つだけ',
       '結果はいらない（質問だけ楽しめれば）',
       'その他'
     ]);

  // ========== S6: 課金意向 ==========
  var pbS6 = form.addPageBreakItem().setTitle('S6. 費用について');

  var q61 = form.addMultipleChoiceItem();
  q61.setTitle('Q6.1 子育ての情報・考え方に、いま 1ヶ月でいくらくらいまでなら払っていますか／払えますか（書籍・有料相談・サブスクなどの合計の感覚で）')
     .setRequired(true)
     .setChoiceValues(['¥0', '〜¥500', '〜¥1,000', '〜¥2,000', '〜¥3,000', '¥3,000超でも内容次第']);

  var q62 = form.addGridItem();
  q62.setTitle('Q6.2 それぞれの形について、お金を出してもよいと思える上限に近いものを（任意）')
     .setRows([
       'a. 年代別の関わり方ガイド（PDF、1冊ごと）',
       'b. 自分に合う考え方を提案する仕組み（1回）',
       'd. 近くで集まれるオフラインの場（1回参加）'
     ])
     .setColumns(['¥0=無料なら', '〜¥500', '〜¥1,000', '〜¥2,000', 'それ以上も', '有料なら使わない']);

  // Q6.2c は CEO決定（高額アンカー回避）により上限〜¥1,000で別設問化
  var q62c = form.addMultipleChoiceItem();
  q62c.setTitle('Q6.2c 毎日/毎週とどく読み物の定期購読（月額）について、お金を出してもよいと思える上限は（任意）')
      .setRequired(false)
      .setChoiceValues(['¥0=無料なら', '〜¥500', '〜¥1,000', '有料なら登録しない']);

  var q63 = form.addMultipleChoiceItem();
  q63.setTitle('Q6.3 もし定期購読（月額）があるとしたら、どれが近いですか（任意）')
     .setRequired(false)
     .setChoiceValues([
       '月額には基本的に登録しない（都度・無料が良い）',
       '〜¥500/月なら検討する',
       '〜¥1,000/月なら内容次第で',
       '〜¥1,500/月でも価値があれば',
       '価格より「中身が自分に合うか」で決める'
     ]);

  var q64 = form.addParagraphTextItem();
  q64.setTitle('Q6.4 お金の感覚について、選択肢では選びにくかった点や「こういう条件なら／こういう中身なら、払う・払わない」があれば一言（任意）')
     .setRequired(false);

  // ========== S7: NOT-do 選好 ==========
  var pbS7 = form.addPageBreakItem().setTitle('S7. 提供のかたちについて');

  var q71 = form.addMultipleChoiceItem();
  q71.setTitle('Q7.1 「教材や玩具などの“物”は郵送されない」ことについて、どう感じますか（任意）')
     .setRequired(false)
     .setChoiceValues([
       '1 物がないなら使わない',
       '2 やや物足りない',
       '3 気にならない',
       '4 むしろ嬉しい（物が増えない）',
       '5 物がないことが選ぶ理由になる'
     ]);

  var q72 = form.addMultipleChoiceItem();
  q72.setTitle('Q7.2 「専用アプリや専用タブレットは不要（note や PDF などで完結）」ことについて、どう感じますか（任意）')
     .setRequired(false)
     .setChoiceValues([
       '1 アプリがないなら使わない',
       '2 やや使いにくそう',
       '3 気にならない',
       '4 むしろ嬉しい',
       '5 アプリ不要は選ぶ理由になる'
     ]);

  // ========== S8: 自由記述・連絡先 ==========
  var pbS8 = form.addPageBreakItem().setTitle('S8. 最後に（任意）');

  var q81 = form.addParagraphTextItem();
  q81.setTitle('Q8.1 「これがあれば使ってみたい」「これがあると使わない」という点があれば一言（任意・1〜2行）')
     .setRequired(false);

  var q82 = form.addTextItem();
  q82.setTitle('Q8.2 β（無料モニター）のご案内を受け取れるメールアドレス（任意）')
     .setHelpText('登録は任意です。少人数のモニター募集時のみご連絡します。広告メールは送りません。')
     .setRequired(false);

  // ========== Sd: 対象外ライト動線（Q1.1の分岐先・1ページ完結→送信）==========
  // CEO決裁 v1.2: 「対象外＝お礼で終了」を廃止。妊娠中・妊活・卒業層を捨てず
  //   ライトなリード受け皿に。本編(S2-S8)には1人も混ぜず集計純度は維持。
  var pbDisq = form.addPageBreakItem()
    .setTitle('ここまでお進みくださり、ありがとうございます')
    .setHelpText(
      '今回の声集めは0〜6歳のお子さまを育てている方を中心にお聞きしていますが、' +
      'これから親になる方・なるかもしれない方の「いま気になっていること」も、私たちにとって大切なヒントです。' +
      'よろしければ、あと少しだけ教えてください（任意・30秒ほど）。お急ぎの方はこのまま送信していただいて大丈夫です。'
    );

  var qd1 = form.addMultipleChoiceItem();
  qd1.setTitle('Qd.1 いまのご状況に近いものは（任意）')
     .setRequired(false)
     .setChoiceValues([
       '妊娠中・出産を控えている',
       'これから子どもを持ちたい／考えている（妊活中を含む）',
       '子どもはもう大きい（小学生以上）',
       '特に予定はない／関心があって見てみた',
       '答えたくない'
     ]);

  var qd2 = form.addParagraphTextItem();
  qd2.setTitle('Qd.2 いま、子育てや子どもとの関わりについて「気になっていること・知りたいこと」があれば一言（任意）')
     .setHelpText('これからのことでも、ばくぜんとしたことでも大丈夫です。空欄でも構いません。')
     .setRequired(false);

  var qd3 = form.addTextItem();
  qd3.setTitle('Qd.3 これからの発信や活動のご案内を受け取れるメールアドレス（任意）')
     .setHelpText('登録は任意です。これからの発信や活動のご案内を、ごくたまにお送りします。広告メールは送りません。')
     .setRequired(false);
  safe('Qd.3 メール形式検証', function () {
    qd3.setValidation(FormApp.createTextValidation().requireTextIsEmail().build());
  });

  var noteLine = 'おわりに ── 日々考えていることは note でゆるやかに発信しています。よろしければ覗いてみてください。';
  if (CONFIG.NOTE_URL) { noteLine += '\n' + CONFIG.NOTE_URL; }
  form.addSectionHeaderItem().setTitle('　').setHelpText(noteLine);

  // 対象外ページ完了で送信終了（本編へは戻さない）
  pbDisq.setGoToPage(SUBMIT);

  // S8 ページ完了後は対象外ページを飛ばして送信
  pbS8.setGoToPage(SUBMIT);

  // Q1.1 の選択肢に分岐ナビゲーションを設定
  //   「子どもはいない／その他」を意向で2分割し妊活・これから層を救う（CEO決裁 v1.2）
  q11.setChoices([
    q11.createChoice('妊娠中（出産予定）', pbDisq),
    q11.createChoice('0歳', CONT),
    q11.createChoice('1〜2歳', CONT),
    q11.createChoice('3〜4歳', CONT),
    q11.createChoice('5〜6歳', CONT),
    q11.createChoice('小学生（7歳以上）', pbDisq),
    q11.createChoice('子どもはいない（これから持ちたい・考え中）', pbDisq),
    q11.createChoice('子どもはいない・その他（いまは予定なし）', pbDisq)
  ]);

  // ========== 送信完了画面 ==========
  form.setConfirmationMessage(
    'ご協力ありがとうございました。いただいた声は、これからの形づくりにそっと活かさせていただきます。' +
    '日々のことや考えていることは note でゆるやかに発信しています。よろしければ覗いてみてください。'
  );

  // ========== 出力 ==========
  var editUrl = form.getEditUrl();
  var pubUrl = form.getPublishedUrl();
  Logger.log('=== ひだまりこそだち インタビューForm 作成完了 ===');
  Logger.log('編集URL（CEO最終目視用・他人に渡さない）: ' + editUrl);
  Logger.log('回答用URL（配布用）: ' + pubUrl);
  Logger.log('設定: REQUIRE_LOGIN=' + CONFIG.REQUIRE_LOGIN + ' / LIMIT_ONE_RESPONSE=' + CONFIG.LIMIT_ONE_RESPONSE);

  return { editUrl: editUrl, publishedUrl: pubUrl };
}
