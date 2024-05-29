base_url = "https://wc.grafia13.fi/wp-content/uploads/2024/05/Taideteos{}.jpg"

# Generate the list of URLs
urls = [base_url.format(i) for i in range(1, 201)]

# Save the URLs to a file
with open("urls.txt", "w") as file:
    for url in urls:
        file.write(url + "\n")
