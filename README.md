# Google <-> VAN trigger

<b>A simple google script that listens to a trigger from a google form, uses said data to find the most relevant VAN ID and sync the results to an output
spreadsheet</b>

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
-   `<VAN KEY>` with your VAN API key
-   `<VAN SURVEY QUESTION>` with the ID of the survey question from VAN
-   `<VAN SURVEY RESPONSE>` with the ID of the response you want applied to the survey question
