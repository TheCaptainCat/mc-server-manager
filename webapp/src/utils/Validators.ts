const emailRe = /^(([^<>()[\].,;:\s@"]+(\.[^<>()[\].,;:\s@"]+)*)|(".+"))@(([^<>()[\].,;:\s@"]+\.)+[^<>()[\].,;:\s@"]{2,})$/i;
const pwRe = /^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#$%^&*])(?=.{8,})/;

export function isValidEmail(value: string) {
  return emailRe.test(String(value).toLocaleLowerCase());
}

export function isValidPassword(value: string) {
  return pwRe.test(String(value).toLocaleLowerCase());
}
