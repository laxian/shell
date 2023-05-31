const request = require('request');
 
const url = 'http://${host}:8888/api/v4/projects?limit=100&skip_pagination=true&skip_namespace=true&compact_mode=true';
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
  for (let index = 0; index < json.length; index++) {
    const element = json[index];
    // console.log(element.name)
  }
  console.log(body);
});