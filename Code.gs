// BEFORE USING:
// make sure you have the `appscript.json` file set up
// that file contains all the permissions that set up the oauth frontend
// see: https://developers.google.com/identity/protocols/oauth2/scopes

function callFormsAPI() {
	// the form you want to monitor. Get ID from URL
	const formId = '<GOOGLE FORM ID>';

	// this will create new triggers each time you run
	// make sure to delete old triggers manually after each run
	ScriptApp.newTrigger('getVanId').forForm(formId).onFormSubmit().create();
}

function getVanId(e) {
	const formResponse = e.response.getItemResponses();

	// get the responses to each field
	// stick it into an object to make it easier to send across to backend
	var formdata = {
		fname: formResponse[0].getResponse(),
		lname: formResponse[1].getResponse(),
		hno: formResponse[2].getResponse(),
		street: formResponse[3].getResponse(),
		zip: formResponse[4].getResponse(),
		phone: formResponse[5].getResponse(),
        v_key: <VAN KEY>,
        v_sq: <VAN SURVEY QUESTION>,
        v_rs: <VAN SURVEY RESPONSE>
	};

	// standard fetch to backend cloudwatch function
	// will fail without `Authorization` header
	const response = UrlFetchApp.fetch('https://lawn-sign-van-trigger-5qfx7x7dta-uc.a.run.app', {
		method: 'post',
		muteHttpExceptions: true,
		contentType: 'application/json',
		payload: JSON.stringify(formdata),
		headers: {
			Authorization: `Bearer ${ScriptApp.getIdentityToken()}`
		}
	});

	// put stuff into spreadsheet by id
	const vanId = response.getContentText();
	const sheetId = '<GOOGLE SHEET ID>';
	const sheetName = '<GOOGLE SHEET NAME>';

	var activeSheet = SpreadsheetApp.openById(sheetId);
	var sheet = activeSheet.getSheetByName(sheetName);
	var cell = 'I' + sheet.getDataRange().getNumRows();
	sheet.getRange(cell).setValue(vanId);

	// write to couldwatch (or whatever google calls it?) logs
	Logger.log(vanId);
}
