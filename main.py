import json
import os
from pprint import pprint

import pandas as pd
from datetime import datetime
import time

df = pd.DataFrame([], columns=['URL', 'SEO', 'Accessibility', 'Best Practices', 'Performance', 'Perf_FCP'])
cwd = os.getcwd()
name = "m24"
getdate = datetime.now().strftime("%m-%d-%y")
df_urls = pd.read_csv("ILURLs.csv")
print(df_urls)
# urls = df_urls.values.tolist()
# print(urls)
count = 1
for row in df_urls:
    row = str(row)
    print(row)
    # print(type(row))
    stream = os.popen(
        'lighthouse ' + row + ' --quiet --no-update-notifier --no-enable-error-reporting --output=json --output-path=' + cwd + '\\' + name + '_' + getdate + '.report.json --chrome-flags="--headless" --preset=desktop')
    print("Report complete for: " + row)
    time.sleep(110)
    file_name = name + '_' + getdate + '.report.json'
    json_filename = cwd + '\\' + name + '_' + getdate + '.report.json'
    with open(json_filename, encoding="mbcs") as json_data:
        loaded_json = json.load(json_data)
    seo = str(round(loaded_json["categories"]["seo"]["score"] * 100))
    accessibility = str(round(loaded_json["categories"]["accessibility"]["score"] * 100))
    best_practices = str(round(loaded_json["categories"]["best-practices"]["score"] * 100))
    performance = str(round(loaded_json["categories"]["performance"]["score"] * 100))
    perf_FCP = ((loaded_json["categories"]["performance"]["auditRefs"][0]["weight"]))

    dictionary1 = {"URL": row, "SEO": seo, "Accessibility": accessibility, "Best Practices": best_practices, "Performance": performance,
                   "Perf_FCP": perf_FCP}
    df = df.append(dictionary1, ignore_index=True).sort_values(by='SEO', ascending=False)

    df.to_csv(cwd + '/lighthouse_' + name + '_' + getdate + '.csv')
    pprint(df)
    new_file_name = name + '_' + getdate + '_' + str(count) + '.report.json'
    os.renames(json_filename, new_file_name)
    count = count + 1
