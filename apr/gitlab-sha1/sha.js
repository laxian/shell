const request = require('request');
 
const url = 'http://${host}:8888/api/v4/projects/57/repository/branches/release';
const options = {
  headers: {
    'PRIVATE-TOKEN': '${gitlab_access_token}'
  }
};

request(url, options, (error, response, body) => {
  if (error) {
    console.error(error);
    return;
  }

  const json = JSON.parse(body);
  console.log(json)
  
  console.log(json.commit.id);
});