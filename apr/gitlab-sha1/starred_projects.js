const request = require('request');
 
const url = 'http://10.10.81.54:8888/api/v4/users/weixian.zhou/starred_projects';
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
  ret = []
  for (let index = 0; index < json.length; index++) {
    const element = json[index];
    ret[index] = {'name': element.name, 'id': element.id}
    // console.log(element.name + ": " + element.id)
  }
  console.log(JSON.stringify(ret));
  // console.log(body);
});