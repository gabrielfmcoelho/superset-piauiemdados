"use client"

import { useEffect } from 'react';
import axios from 'axios';
import { embedDashboard } from '@superset-ui/embedded-sdk';

const supersetUrl = 'http://localhost:8088';
const supersetApiUrl = supersetUrl + '/api/v1/security';
const dashboardId = '304c9ba7-6816-4296-b3d8-968c8b31b021';

async function getToken() {
  // Calling login to get access token
  const loginBody = {
    password: 'admin',
    provider: 'db',
    refresh: true,
    username: 'admin',
  };

  const loginHeaders = {
    headers: {
      'Content-Type': 'application/json',
      Accept: 'application/json',
    },
  };

  const { data } = await axios.post(supersetApiUrl + '/login', loginBody, loginHeaders);
  const accessToken = data['access_token'];

  // Calling guest token
  const guestTokenBody = JSON.stringify({
    resources: [
      {
        type: 'dashboard',
        id: dashboardId,
      },
    ],
    rls: [],
    user: {
      username: 'admin',
      first_name: 'Superset',
      last_name: 'admin',
    },
  });

  const guestTokenHeaders = {
    headers: {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
      Authorization: 'Bearer ' + accessToken,
    },
  };

  const guestTokenResponse = await axios.post(supersetApiUrl + '/guest_token/', guestTokenBody, guestTokenHeaders);
  const guestToken = guestTokenResponse.data['token'];

  embedDashboard({
    id: dashboardId, // given by the Superset embedding UI
    supersetDomain: supersetUrl,
    mountPoint: document.getElementById('superset-container')!, // HTML element in which iframe render
    fetchGuestToken: () => guestToken,
    dashboardUiConfig: { hideTitle: true },
  });

  const iframe = document.querySelector('iframe');
  if (iframe) {
    iframe.style.width = '100%'; // Set the width as needed
    iframe.style.minHeight = '100vw'; // Set the height as needed
  }
}

const Page: React.FC = () => {
  useEffect(() => {
    getToken();
  }, []);

  return (
    <div className="App">
      <div id="superset-container"></div>
    </div>
  );
};

export default Page;
