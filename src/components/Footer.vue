<template>
  <div col right-0 fixed>
    <div my-4>
       <Dark />
    </div>
    <RouterLink my-4 class="icon-btn mx-2" to="/">
      <div i-carbon-home />
    </RouterLink>

 

    <RouterLink my-4 class="icon-btn mx-2" to="/blog">
      <div i-carbon-dicom-overlay />
    </RouterLink>

    <a
      my-4
      class="icon-btn mx-2"
      rel="noreferrer"
      href="https://smartprocloud.auth.us-east-1.amazoncognito.com/login?client_id=6d4rt7sphoaihhcj5on3ghb727&response_type=code&scope=aws.cognito.signin.user.admin+email+openid+phone+profile&redirect_uri=https%3A%2F%2Fsmartpro.cloud%2Ftoken"
      target="_blank"
      title="CloudApi"
    >
      <i class = "mdi mdi-account text-lg"></i>
    </a>
  </div>
</template>
