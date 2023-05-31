const request = require('request');
const fs = require('fs');

var projs
fs.readFile('./starred_proj_names.txt', 'utf8', (err, data) => {
  if (err) {
    console.error(err);
    return;
  }

  projs = JSON.parse(data)

  for (let index = 0; index < projs.length; index++) {
    const proj = projs[index];
    id = proj.id;
    pname = proj.name;
    // console.log(pname)

    branch = 'release'
    if ([85].includes(id)) {
      branch = 'release_gx_x64'
    }
    if ([82].includes(id)) {
      branch = 'release_gx'
    }
  
    const url = `http://10.10.81.54:8888/api/v4/projects/${id}/repository/branches/${branch}`;
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
      console.log(url + ': ' + json.commit.short_id);
    });
  }
  
});



