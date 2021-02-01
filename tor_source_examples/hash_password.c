/**
from the upsteam tor project.

This is the example code for ControlHashPassword that needs to be ported to
python
**/

/** https://github.com/torproject/tor/blob/master/src/app/main/main.c **/

#include "lib/crypt_ops/crypto_s2k.h"

/** Entry point for password hashing: take the desired password from
 * the command line, and print its salted hash to stdout. **/

static void
do_hash_password(void)
{

  char output[256];
  char key[S2K_RFC2440_SPECIFIER_LEN+DIGEST_LEN];

  crypto_rand(key, S2K_RFC2440_SPECIFIER_LEN-1);
  key[S2K_RFC2440_SPECIFIER_LEN-1] = (uint8_t)96; /* Hash 64 K of data. */
  secret_to_key_rfc2440(key+S2K_RFC2440_SPECIFIER_LEN, DIGEST_LEN,
                get_options()->command_arg, strlen(get_options()->command_arg),
                key);
  base16_encode(output, sizeof(output), key, sizeof(key));
  printf("16:%s\n",output);
}
