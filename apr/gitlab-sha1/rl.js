const fs = require('fs');

// const data = fs.readFileSync('./starred_proj_names.txt', 'utf8');
const projs = [{"name":"AppRestaurant","id":475},{"name":"robotRemoteOta","id":318},{"name":"app-apr-mirror","id":302},{"name":"app-apr-food-deliver","id":236},{"name":"GxAppService","id":135},{"name":"VisionService","id":85},{"name":"ConnectionService","id":84},{"name":"VoiceService","id":83},{"name":"ControlService","id":82},{"name":"GxSystemDevKit","id":75},{"name":"SegwayProvision","id":61},{"name":"GX_Service","id":57}]

const fetch = (...args) => import('node-fetch').then(({default: fetch}) => fetch(...args));

for (const proj of projs) {
	const id = proj.id;
	const pname = proj.name;
      
	let branch = 'release';
	if ([85].includes(id)) {
	  branch = 'release_gx_x64';
	}
	if ([82].includes(id)) {
	  branch = 'release_gx';
	}

	const url = `http://${host}:8888/api/v4/projects/${id}/repository/branches/${branch}`;
	// console.log(url);
	const options = {
	  headers: {
	    'PRIVATE-TOKEN': '${gitlab_access_token}'
	  }
	};
      
	fetch(url, options)
	  .then((response) => {
	    if (!response.ok) {
		// console.log(response.statusText);
	      throw new Error(`${proj.name}-${branch} --> HTTP error! status: ${response.status}\nMaybe error branch`);
	    }
	    return response.json();
	  })
	  .then((json) => {
	    console.log(`${proj.name}-${branch}: ${json.commit.short_id}`);
	  })
	  .catch((err) => {
	    console.error(err);
	  });
      }