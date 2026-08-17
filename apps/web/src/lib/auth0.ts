import { Auth0Client } from "@auth0/nextjs-auth0/server";

let client: Auth0Client | null = null;

export function getAuth0Client(): Auth0Client {
  if (client) {
    return client;
  }
  client = new Auth0Client({
    authorizationParameters: {
      ...(process.env.AUTH0_AUDIENCE ? { audience: process.env.AUTH0_AUDIENCE } : {}),
      scope: "openid profile email",
    },
    enableAccessTokenEndpoint: true,
  });
  return client;
}
