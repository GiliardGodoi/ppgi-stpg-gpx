import requests
import os

problems_class = {
        'b' : {'max' : 18},
        'c' : {'max' : 20},
        'd' : {'max' : 20},
        'e' : {'max' : 20},
        'others' : ['dv80.txt', 'dv160.txt', 'dv320.txt' ]
    }


def download(file_name):

    url = f'http://people.brunel.ac.uk/~mastjjb/jeb/orlib/files/{file_name}'
    response = requests.get(url)
    data = response.content

    return data

def save(content, file_name, folder):

    local = os.path.join(folder, file_name)

    with open(local, "wb") as file:
        file.write(content)

    return True


def generate_file_names(key = None):

    if isinstance(problems_class[key], list) :
        for item in problems_class[key]:
            yield item
    elif isinstance(problems_class[key], dict) :
        counter = 1
        MAX = problems_class[key]['max']
        while counter <= MAX :
            yield f"stein{key}{counter}.txt"
            counter += 1

if __name__ == "__main__":
    print('start download...')

    OUTPUT_FOLDER = os.path.join('ORLibrary')

    if not os.path.exists(OUTPUT_FOLDER):
        os.mkdir(OUTPUT_FOLDER)
    # else :
    #     if os.listdir(OUTPUT_FOLDER):
    #         raise Exception("Output folder is not empty")

    count = 1

    ## DOWNLOAD ALL FILES
    # for key in problems_class.keys():
    #     for file_name in generate_file_names(key):
    #         data = download(file_name)
    #         save(data, file_name, OUTPUT_FOLDER)
    #         print(f'files: {count}', end="\r")
    #         count += 1

    ## DOWNLOAD ONLY PROBLEMS FROM A ONE CLASS
    for file_name in generate_file_names('others'):
            data = download(file_name)
            save(data, file_name, OUTPUT_FOLDER)
            print(f'files: {count}', end="\r")
            count += 1

    count -= 1
    print(f'Obtained {count} files.')

