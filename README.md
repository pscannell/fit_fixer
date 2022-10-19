# Fit File Fixer

Tool to fix broken timestamps in Cycplus/XOSS generated fit files & upload results to Strava.

## Summary

In many cases, Fit files generated from Cycplus/XOSS bicycle computers will generate an incorrect starting timestamp for each activity. This can lead to multiple activities being misidentified as a single activity, which can disrupt uploads to tools like Strava.

## Getting started

### Dependencies

#### Python

* Tested using python >=3.10
* Install python dependencies
  
  * ```bash
    pip install -r requirements.txt
    ```

#### Java

* FitTool requires Java runtime (JRE) install. Follow instructions [here](https://docs.oracle.com/goldengate/1212/gg-winux/GDRAD/java.htm#BGBFJHAB) to install Java runtime.

### Strava support

* The Strava upload integration is managed by the Strava API. Ensure you register for a Strava developer account by following these [instructions](https://developers.strava.com/docs/getting-started/#account).
* Copy the generated Strava API credentials locally to this folder at "./.strava_config.json"
* After creating an API & adding credentials locally, you must authorize the API once using these [instructions](https://developers.strava.com/docs/getting-started/#oauth).

### Example

Use the following command to clean a broken Fit file & upload to Strava:

```bash
python main.py -f <MY_FIT_FILE_PATH>
```
