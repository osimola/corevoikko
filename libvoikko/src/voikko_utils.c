/* Libvoikko: Finnish spellchecker and hyphenator library
 * Copyright (C) 2006 Harri Pitkänen <hatapitk@iki.fi>
 *
 * This program is free software; you can redistribute it and/or
 * modify it under the terms of the GNU General Public License
 * as published by the Free Software Foundation; either version 2
 * of the License, or (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
 *********************************************************************************/

#include "voikko_defs.h"
#include "voikko_utils.h"
#include "voikko_setup.h"
#include <stdlib.h>
#include <string.h>
#include <wctype.h>

#ifndef HAVE_ICONV
  #ifdef WIN32
    #include <windows.h>
  #endif
#endif

wchar_t * voikko_cstrtoucs4(const char * word, const char * encoding, size_t len) {
#ifdef HAVE_ICONV
	iconv_t cd;
	int using_temporary_converter = 0;
	size_t conv_bytes;
	wchar_t * ucs4_buffer = malloc((LIBVOIKKO_MAX_WORD_CHARS + 1) * sizeof(wchar_t));
	if (ucs4_buffer == 0) return 0;
	size_t res_size;
	char * outptr = (char *) ucs4_buffer;
	ICONV_CONST char * inptr = (ICONV_CONST char *) word;
	size_t inbytesleft;
	size_t outbytesleft = LIBVOIKKO_MAX_WORD_CHARS * sizeof(wchar_t);
	ucs4_buffer[LIBVOIKKO_MAX_WORD_CHARS] = L'\0';
	
	if (len == 0) len = strlen(word);
	inbytesleft = len;
	
	if (strcmp(encoding, "UTF-8") == 0) cd = voikko_options.iconv_utf8_ucs4;
	else if (strcmp(encoding, voikko_options.encoding) == 0) cd = voikko_options.iconv_ext_ucs4;
	else {
		cd = iconv_open(INTERNAL_CHARSET, encoding);
		if (cd == (iconv_t) -1) {
			free(ucs4_buffer);
			return 0;
		}
		using_temporary_converter = 1;
	}
	
	LOG(("voikko_cstrtoucs4\n"));
	LOG(("inbytesleft = %d\n", (int) inbytesleft));
	LOG(("outbytesleft = %d\n", (int) outbytesleft));
	LOG(("inptr = '%s'\n", inptr));
	iconv(cd, 0, &inbytesleft, &outptr, &outbytesleft);
	conv_bytes = iconv(cd, &inptr, &inbytesleft, &outptr, &outbytesleft);
	LOG(("conv_bytes = %d\n", (int) conv_bytes));
	LOG(("inbytesleft = %d\n", (int) inbytesleft));
	LOG(("outbytesleft = %d\n", (int) outbytesleft));
	LOG(("inptr = '%s'\n", inptr));
	if (conv_bytes == -1) {
		if (using_temporary_converter) iconv_close(cd);
		free(ucs4_buffer);
		return 0;
	}
	
	if (using_temporary_converter) iconv_close(cd);
	*((wchar_t *) outptr) = L'\0'; /* terminate the output buffer */
	LOG(("ucs4_buffer = '%ls'\n", ucs4_buffer));
	res_size = ((size_t) outptr) - ((size_t) ucs4_buffer) + sizeof(wchar_t);
	ucs4_buffer = realloc(ucs4_buffer, res_size);
	return ucs4_buffer;
#else
  #ifdef WIN32
	int cp;
	if (strcmp(encoding, "UTF-8") == 0) cp = CP_UTF8;
	else if (strcmp(encoding, "CP850") == 0) cp = 850;
	else return 0;
	// On Windows we actually use UTF-16 data internally, so two units may be needed to
	// represent a single character.
	size_t buflen = (LIBVOIKKO_MAX_WORD_CHARS * 2 + 1);
	wchar_t * ucs4_buffer = malloc(buflen * sizeof(wchar_t));
	if (ucs4_buffer == 0) return 0;
	// Illegal characters are ignored, because MB_ERR_INVALID_CHARS is not supported
	// before WIN2K_SP4.
	int result = MultiByteToWideChar(cp, 0, word, len, ucs4_buffer, buflen - 1);
	if (result == 0) {
		free(ucs4_buffer);
		return 0;
	}
	else {
		ucs4_buffer[result] = L'\0';
		return ucs4_buffer;
	}
  #endif //WIN32
#endif //HAVE_ICONV
}

char * voikko_ucs4tocstr(const wchar_t * word, const char * encoding, size_t len) {
#ifdef HAVE_ICONV
	iconv_t cd;
	int using_temporary_converter = 0;
	size_t conv_bytes;
	char * utf8_buffer = malloc(LIBVOIKKO_MAX_WORD_CHARS * 6 + 1);
	if (utf8_buffer == 0) return 0;
	size_t res_size;
	char * outptr = utf8_buffer;
	ICONV_CONST char * inptr = (ICONV_CONST char *) word;
	size_t inbytesleft;
	size_t outbytesleft = LIBVOIKKO_MAX_WORD_CHARS;
	utf8_buffer[LIBVOIKKO_MAX_WORD_CHARS] = '\0';
	
	if (len == 0) len = wcslen(word);
	inbytesleft = len * sizeof(wchar_t);
	
	if (strcmp(encoding, "UTF-8") == 0) cd = voikko_options.iconv_ucs4_utf8;
	else if (strcmp(encoding, voikko_options.encoding) == 0) cd = voikko_options.iconv_ucs4_ext;
	else {
		cd = iconv_open(encoding, INTERNAL_CHARSET);
		if (cd == (iconv_t) -1) {
			free(utf8_buffer);
			return 0;
		}
		using_temporary_converter = 1;
	}
	
	LOG(("voikko_ucs4tocstr\n"));
	LOG(("inbytesleft = %d\n", (int) inbytesleft));
	LOG(("outbytesleft = %d\n", (int) outbytesleft));
	LOG(("inptr = '%s'\n", inptr));
	iconv(cd, 0, &inbytesleft, &outptr, &outbytesleft);
	conv_bytes = iconv(cd, &inptr, &inbytesleft, &outptr, &outbytesleft);
	LOG(("conv_bytes = %d\n", (int) conv_bytes));
	LOG(("inbytesleft = %d\n", (int) inbytesleft));
	LOG(("outbytesleft = %d\n", (int) outbytesleft));
	LOG(("inptr = '%s'\n", inptr));
	if (conv_bytes == -1) {
		if (using_temporary_converter) iconv_close(cd);
		free(utf8_buffer);
		return 0;
	}
	if (using_temporary_converter) iconv_close(cd);
	*outptr = '\0'; /* terminate the output buffer */
	LOG(("utf8_buffer = '%s'\n", utf8_buffer));
	res_size = ((size_t) outptr) - ((size_t) utf8_buffer) + 1;
	utf8_buffer = realloc(utf8_buffer, res_size);
	return utf8_buffer;
#else
  #ifdef WIN32
	int cp;
  	if (strcmp(encoding, "UTF-8") == 0) cp = CP_UTF8;
	else if (strcmp(encoding, "CP850") == 0) cp = 850;
	else return 0;
  	size_t buflen = LIBVOIKKO_MAX_WORD_CHARS * 6 + 1;
  	char * utf8_buffer = malloc(buflen);
  	if (utf8_buffer == 0) return 0;
  	int result = WideCharToMultiByte(cp, 0, word, -1, utf8_buffer, buflen - 1, 0, 0);
  	if (result == 0) {
		free(utf8_buffer);
		return 0;
	}
	else {
		utf8_buffer[result] = '\0';
		return utf8_buffer;
	}
  #endif //WIN32
#endif //HAVE_ICONV
}

int voikko_hash(const wchar_t * word, size_t len, int order) {
	int hash = 0;
	size_t counter;
	for (counter = 0; counter < len; counter++) {
		hash = (hash * 37 + word[counter]) % (1 << order);
	}
	return hash;
}

enum casetype voikko_casetype(const wchar_t * word, size_t nchars) {
	int first_uc = 0;
	int rest_lc = 1;
	int all_uc = 1;
	int no_letters = 1;
	int i;
	if (nchars == 0) return CT_NO_LETTERS;
	if (iswupper(word[0])) {
		first_uc = 1;
		no_letters = 0;
	}
	if (iswlower(word[0])) {
		all_uc = 0;
		no_letters = 0;
	}
	for (i = 1; i < nchars; i++) {
		if (iswupper(word[i])) {
			no_letters = 0;
			rest_lc = 0;
		}
		if (iswlower(word[i])) {
			all_uc = 0;
			no_letters = 0;
		}
	}
	if (no_letters) return CT_NO_LETTERS;
	if (all_uc) return CT_ALL_UPPER;
	if (!rest_lc) return CT_COMPLEX;
	if (first_uc) return CT_FIRST_UPPER;
	else return CT_ALL_LOWER;
}

void voikko_set_case(enum casetype charcase, wchar_t * word, size_t nchars) {
	size_t i;
	if (nchars == 0) return;
	switch (charcase) {
		case CT_NO_LETTERS:
		case CT_COMPLEX:
			return; /* Do nothing */
		case CT_ALL_LOWER:
			for (i = 0; i < nchars; i++) word[i] = towlower(word[i]);
			return;
		case CT_ALL_UPPER:
			for (i = 0; i < nchars; i++) word[i] = towupper(word[i]);
			return;
		case CT_FIRST_UPPER:
			word[0] = towupper(word[0]);
			for (i = 1; i < nchars; i++) word[i] = towlower(word[i]);
			return;
	}
}
