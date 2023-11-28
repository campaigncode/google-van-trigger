# Google <-> VAN trigger

<b>A simple google script that listens to a trigger from a google form, uses said data to apply a survey response in VAN, and syncs the results to an output
google spreadsheet</b>

## Prerequisites

-   A google form that gets at least the following information from the voter. Each value must be a separate field, in the following order:
    -   First name
    -   Last name
    -   House number
    -   Street address
    -   Zip code
    -   Phone number
-   Results linked from the google form to a google sheet
-   A google [Apps Script](https://script.google.com/home/projects/) project initialised
-   A google [Cloud](https://console.cloud.google.com/functions) project initialised

# Trigger:

The "trigger" script is a Google App Script that runs every time the form is submitted. It retrieves form data from the form, formats it appropriately and hands
it over to the "handler" to process the VAN side of the request. The handler then returns a VAN ID back to the trigger script that is then added to the output
google sheet by the trigger.

## Setup

1. Create a file called `appscript.json` under <i>Files</i> in the project
2. Copy code from `appscript.json` in this repository to `appscript.json` in your project. Save the file
3. Create a file called `Code.gs` under <i>Files</i> in the project
4. Copy all code from `Cods.gs` in this repository to `Code.gs` in your project

## Configuration

In `Code.gs`, replace:

-   `<GOOGLE FORM ID>` with the ID from the Google Form URL
-   `<GOOGLE SHEET ID>` with the ID from the Google Sheet URL
-   `<GOOGLE SHEET NAME>` with the name of the active sheet in the Google Form responses sheet
-   `<VAN SURVEY QUESTION>` with the ID of the survey question from VAN
-   `<VAN SURVEY RESPONSE>` with the ID of the response you want applied to the survey question

## Deployment

-   Once setup and configuration is complete, click run. Make sure to click run only once! Else, you will create multiple triggers for the same form and the
    code will run multiple times, potentially causing errors.
-   For use with another form, copy `Code.gs` into a new file, say `Code2.gs` and go through the setup, configuration and deploy steps again. You will need one
    file per form you want to listen to.

# Handler:

The "handler" is a google cloud function that listens for events from the trigger. It takes the data sent to it by the trigger (now properly formatted), finds
the voter based on the information supplied in the form (name, address etc.) and adds the survey question and response defined in the trigger to the voter in
VAN. It then returns the VAN ID of the voter from VAN to the trigger.

## Setup

1. Create a new Google Cloud Function
2. Copy code from `backend.py` to your new Cloud Function
3. Save the function and copy its URL
4. Replace `<HANDLER URL>` in your trigger script with this URL

## Configuration

-   In the Cloud Function, replace:
    -   `<VAN KEY>` with your VAN API key

## Deployment

-   You only need one handler per committee. Multiple forms can use the same handler and there is no need to deploy another handler if you want to add a new
    trigger for a new form.
