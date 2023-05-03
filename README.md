
OlxScraper: 
 - Collects data from Olx
 - Shows the collected data to users
 - Different data is shown depending on the user's access level
- The user can delete uninteresting ads, he deletes them only for himself

How to run: 
```bash
git clone 'https://github.com/serhiion/OLX.git'
```

```bash
sudo docker compose build
```

```bash
sudo docker compose up
```
If the error "connection refused" occurs, run
```bash
sudo docker compose down
```
```bash
sudo docker compose up
```