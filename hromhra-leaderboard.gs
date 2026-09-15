/**
 * HROM HRA — rebríček a zber e-mailov do Google tabuľky
 * ====================================================
 * Návod na nasadenie je v súbore leaderboard-navod.md.
 *
 * Tento skript robí dve veci:
 *   1) ukladá meno, e-mail a skóre hráča do tabuľky (jeden riadok na e-mail),
 *   2) vracia TOP hráčov pre rebríček na stránke.
 */

var HARKOK = 'Hraci';   // názov hárka v tabuľke
var TOP_N  = 10;        // koľko hráčov sa zobrazí v rebríčku

function doGet(e) {
  var akcia = (e && e.parameter && e.parameter.action) || 'top';
  if (akcia === 'top') {
    return json({ ok: true, top: top() });
  }
  return json({ ok: false, error: 'Neznáma akcia.' });
}

function doPost(e) {
  var data;
  try {
    data = JSON.parse(e.postData.contents);
  } catch (err) {
    return json({ ok: false, error: 'Neplatné dáta.' });
  }

  if (data.action !== 'save') {
    return json({ ok: false, error: 'Neznáma akcia.' });
  }

  var meno  = String(data.meno || '').trim().slice(0, 40);
  var email = String(data.email || '').trim().toLowerCase().slice(0, 120);
  var skore = Math.max(0, Math.min(100, parseInt(data.skore, 10) || 0));

  if (!meno || email.indexOf('@') === -1) {
    return json({ ok: false, error: 'Chýba meno alebo e-mail.' });
  }

  // zámok, aby si dvaja hráči naraz neprepísali riadok
  var lock = LockService.getScriptLock();
  lock.waitLock(20000);
  try {
    var sh = harok();
    var hodnoty = sh.getDataRange().getValues();
    var riadok = -1;

    for (var i = 1; i < hodnoty.length; i++) {
      if (String(hodnoty[i][2]).trim().toLowerCase() === email) { riadok = i + 1; break; }
    }

    var teraz = new Date();
    if (riadok === -1) {
      sh.appendRow([teraz, meno, email, skore, teraz]);
    } else {
      sh.getRange(riadok, 2).setValue(meno);
      // skóre len zvyšujeme, nikdy neznižujeme
      var stare = parseInt(sh.getRange(riadok, 4).getValue(), 10) || 0;
      if (skore > stare) sh.getRange(riadok, 4).setValue(skore);
      sh.getRange(riadok, 5).setValue(teraz);
    }
  } finally {
    lock.releaseLock();
  }

  return json({ ok: true, top: top() });
}

function top() {
  var sh = harok();
  var hodnoty = sh.getDataRange().getValues();
  var hraci = [];

  for (var i = 1; i < hodnoty.length; i++) {
    var meno  = String(hodnoty[i][1] || '').trim();
    var email = String(hodnoty[i][2] || '').trim();
    var skore = parseInt(hodnoty[i][3], 10) || 0;
    if (!email) continue;
    hraci.push({ meno: meno || 'Hráč', email: email, skore: skore });
  }

  hraci.sort(function (a, b) { return b.skore - a.skore; });
  return hraci.slice(0, TOP_N);
}

function harok() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sh = ss.getSheetByName(HARKOK);
  if (!sh) {
    sh = ss.insertSheet(HARKOK);
    sh.appendRow(['Prihlásený', 'Meno', 'E-mail', 'Skóre', 'Naposledy hral']);
    sh.setFrozenRows(1);
  }
  return sh;
}

function json(obj) {
  return ContentService
    .createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}
