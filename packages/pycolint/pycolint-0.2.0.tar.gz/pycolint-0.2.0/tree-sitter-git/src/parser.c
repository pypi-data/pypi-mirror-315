#include "tree_sitter/parser.h"

#if defined(__GNUC__) || defined(__clang__)
#pragma GCC diagnostic ignored "-Wmissing-field-initializers"
#endif

#define LANGUAGE_VERSION 14
#define STATE_COUNT 21
#define LARGE_STATE_COUNT 2
#define SYMBOL_COUNT 13
#define ALIAS_COUNT 0
#define TOKEN_COUNT 8
#define EXTERNAL_TOKEN_COUNT 0
#define FIELD_COUNT 0
#define MAX_ALIAS_SEQUENCE_LENGTH 5
#define PRODUCTION_ID_COUNT 1

enum ts_symbol_identifiers {
  anon_sym_BANG = 1,
  anon_sym_COLON = 2,
  sym_word = 3,
  anon_sym_LPAREN = 4,
  anon_sym_RPAREN = 5,
  sym_symbol = 6,
  sym_dot = 7,
  sym_hdr = 8,
  sym_type = 9,
  sym_scope = 10,
  sym_descr = 11,
  aux_sym_descr_repeat1 = 12,
};

static const char * const ts_symbol_names[] = {
  [ts_builtin_sym_end] = "end",
  [anon_sym_BANG] = "!",
  [anon_sym_COLON] = ": ",
  [sym_word] = "word",
  [anon_sym_LPAREN] = "(",
  [anon_sym_RPAREN] = ")",
  [sym_symbol] = "symbol",
  [sym_dot] = "dot",
  [sym_hdr] = "hdr",
  [sym_type] = "type",
  [sym_scope] = "scope",
  [sym_descr] = "descr",
  [aux_sym_descr_repeat1] = "descr_repeat1",
};

static const TSSymbol ts_symbol_map[] = {
  [ts_builtin_sym_end] = ts_builtin_sym_end,
  [anon_sym_BANG] = anon_sym_BANG,
  [anon_sym_COLON] = anon_sym_COLON,
  [sym_word] = sym_word,
  [anon_sym_LPAREN] = anon_sym_LPAREN,
  [anon_sym_RPAREN] = anon_sym_RPAREN,
  [sym_symbol] = sym_symbol,
  [sym_dot] = sym_dot,
  [sym_hdr] = sym_hdr,
  [sym_type] = sym_type,
  [sym_scope] = sym_scope,
  [sym_descr] = sym_descr,
  [aux_sym_descr_repeat1] = aux_sym_descr_repeat1,
};

static const TSSymbolMetadata ts_symbol_metadata[] = {
  [ts_builtin_sym_end] = {
    .visible = false,
    .named = true,
  },
  [anon_sym_BANG] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_COLON] = {
    .visible = true,
    .named = false,
  },
  [sym_word] = {
    .visible = true,
    .named = true,
  },
  [anon_sym_LPAREN] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_RPAREN] = {
    .visible = true,
    .named = false,
  },
  [sym_symbol] = {
    .visible = true,
    .named = true,
  },
  [sym_dot] = {
    .visible = true,
    .named = true,
  },
  [sym_hdr] = {
    .visible = true,
    .named = true,
  },
  [sym_type] = {
    .visible = true,
    .named = true,
  },
  [sym_scope] = {
    .visible = true,
    .named = true,
  },
  [sym_descr] = {
    .visible = true,
    .named = true,
  },
  [aux_sym_descr_repeat1] = {
    .visible = false,
    .named = false,
  },
};

static const TSSymbol ts_alias_sequences[PRODUCTION_ID_COUNT][MAX_ALIAS_SEQUENCE_LENGTH] = {
  [0] = {0},
};

static const uint16_t ts_non_terminal_alias_map[] = {
  0,
};

static const TSStateId ts_primary_state_ids[STATE_COUNT] = {
  [0] = 0,
  [1] = 1,
  [2] = 2,
  [3] = 3,
  [4] = 4,
  [5] = 5,
  [6] = 6,
  [7] = 7,
  [8] = 8,
  [9] = 9,
  [10] = 10,
  [11] = 11,
  [12] = 12,
  [13] = 13,
  [14] = 14,
  [15] = 15,
  [16] = 16,
  [17] = 17,
  [18] = 18,
  [19] = 19,
  [20] = 20,
};

static TSCharacterRange sym_symbol_character_set_1[] = {
  {' ', '!'}, {'#', '%'}, {'(', ')'}, {'+', '-'}, {'/', '/'}, {':', '>'}, {'@', '@'}, {'^', '_'},
  {'{', '{'}, {'}', '~'},
};

static bool ts_lex(TSLexer *lexer, TSStateId state) {
  START_LEXER();
  eof = lexer->eof(lexer);
  switch (state) {
    case 0:
      if (eof) ADVANCE(3);
      if (lookahead == '!') ADVANCE(4);
      if (lookahead == '(') ADVANCE(7);
      if (lookahead == ')') ADVANCE(8);
      if (lookahead == '.') ADVANCE(11);
      if (lookahead == ':') ADVANCE(1);
      if (('\t' <= lookahead && lookahead <= '\r') ||
          lookahead == ' ') SKIP(0);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(6);
      END_STATE();
    case 1:
      if (lookahead == ' ') ADVANCE(5);
      END_STATE();
    case 2:
      if (eof) ADVANCE(3);
      if (lookahead == ' ') ADVANCE(10);
      if (lookahead == '.') ADVANCE(11);
      if (lookahead == '-' ||
          lookahead == '_') ADVANCE(6);
      if (('\t' <= lookahead && lookahead <= '\r')) SKIP(2);
      if (set_contains(sym_symbol_character_set_1, 10, lookahead)) ADVANCE(9);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(6);
      END_STATE();
    case 3:
      ACCEPT_TOKEN(ts_builtin_sym_end);
      END_STATE();
    case 4:
      ACCEPT_TOKEN(anon_sym_BANG);
      END_STATE();
    case 5:
      ACCEPT_TOKEN(anon_sym_COLON);
      END_STATE();
    case 6:
      ACCEPT_TOKEN(sym_word);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(6);
      END_STATE();
    case 7:
      ACCEPT_TOKEN(anon_sym_LPAREN);
      END_STATE();
    case 8:
      ACCEPT_TOKEN(anon_sym_RPAREN);
      END_STATE();
    case 9:
      ACCEPT_TOKEN(sym_symbol);
      END_STATE();
    case 10:
      ACCEPT_TOKEN(sym_symbol);
      if (lookahead == ' ') ADVANCE(10);
      if (lookahead == '-' ||
          lookahead == '_') ADVANCE(6);
      if (set_contains(sym_symbol_character_set_1, 10, lookahead)) ADVANCE(9);
      END_STATE();
    case 11:
      ACCEPT_TOKEN(sym_dot);
      END_STATE();
    default:
      return false;
  }
}

static const TSLexMode ts_lex_modes[STATE_COUNT] = {
  [0] = {.lex_state = 0},
  [1] = {.lex_state = 0},
  [2] = {.lex_state = 2},
  [3] = {.lex_state = 2},
  [4] = {.lex_state = 2},
  [5] = {.lex_state = 0},
  [6] = {.lex_state = 2},
  [7] = {.lex_state = 2},
  [8] = {.lex_state = 2},
  [9] = {.lex_state = 2},
  [10] = {.lex_state = 0},
  [11] = {.lex_state = 0},
  [12] = {.lex_state = 0},
  [13] = {.lex_state = 0},
  [14] = {.lex_state = 0},
  [15] = {.lex_state = 0},
  [16] = {.lex_state = 0},
  [17] = {.lex_state = 0},
  [18] = {.lex_state = 0},
  [19] = {.lex_state = 0},
  [20] = {.lex_state = 0},
};

static const uint16_t ts_parse_table[LARGE_STATE_COUNT][SYMBOL_COUNT] = {
  [0] = {
    [ts_builtin_sym_end] = ACTIONS(1),
    [anon_sym_BANG] = ACTIONS(1),
    [anon_sym_COLON] = ACTIONS(1),
    [sym_word] = ACTIONS(1),
    [anon_sym_LPAREN] = ACTIONS(1),
    [anon_sym_RPAREN] = ACTIONS(1),
    [sym_dot] = ACTIONS(1),
  },
  [1] = {
    [sym_hdr] = STATE(15),
    [sym_type] = STATE(5),
    [sym_word] = ACTIONS(3),
  },
};

static const uint16_t ts_small_parse_table[] = {
  [0] = 4,
    ACTIONS(7), 1,
      sym_dot,
    STATE(8), 1,
      aux_sym_descr_repeat1,
    STATE(18), 1,
      sym_descr,
    ACTIONS(5), 2,
      sym_word,
      sym_symbol,
  [14] = 4,
    ACTIONS(7), 1,
      sym_dot,
    STATE(8), 1,
      aux_sym_descr_repeat1,
    STATE(17), 1,
      sym_descr,
    ACTIONS(5), 2,
      sym_word,
      sym_symbol,
  [28] = 4,
    ACTIONS(7), 1,
      sym_dot,
    STATE(8), 1,
      aux_sym_descr_repeat1,
    STATE(20), 1,
      sym_descr,
    ACTIONS(5), 2,
      sym_word,
      sym_symbol,
  [42] = 4,
    ACTIONS(9), 1,
      anon_sym_BANG,
    ACTIONS(11), 1,
      anon_sym_COLON,
    ACTIONS(13), 1,
      anon_sym_LPAREN,
    STATE(11), 1,
      sym_scope,
  [55] = 2,
    ACTIONS(15), 1,
      ts_builtin_sym_end,
    ACTIONS(17), 3,
      sym_word,
      sym_symbol,
      sym_dot,
  [64] = 2,
    STATE(7), 1,
      aux_sym_descr_repeat1,
    ACTIONS(19), 3,
      sym_word,
      sym_symbol,
      sym_dot,
  [73] = 3,
    ACTIONS(24), 1,
      sym_dot,
    STATE(7), 1,
      aux_sym_descr_repeat1,
    ACTIONS(22), 2,
      sym_word,
      sym_symbol,
  [84] = 2,
    ACTIONS(26), 1,
      ts_builtin_sym_end,
    ACTIONS(17), 3,
      sym_word,
      sym_symbol,
      sym_dot,
  [93] = 1,
    ACTIONS(28), 3,
      anon_sym_BANG,
      anon_sym_COLON,
      anon_sym_LPAREN,
  [99] = 2,
    ACTIONS(30), 1,
      anon_sym_BANG,
    ACTIONS(32), 1,
      anon_sym_COLON,
  [106] = 1,
    ACTIONS(34), 2,
      anon_sym_BANG,
      anon_sym_COLON,
  [111] = 1,
    ACTIONS(32), 1,
      anon_sym_COLON,
  [115] = 1,
    ACTIONS(36), 1,
      sym_word,
  [119] = 1,
    ACTIONS(38), 1,
      ts_builtin_sym_end,
  [123] = 1,
    ACTIONS(40), 1,
      anon_sym_RPAREN,
  [127] = 1,
    ACTIONS(42), 1,
      ts_builtin_sym_end,
  [131] = 1,
    ACTIONS(44), 1,
      ts_builtin_sym_end,
  [135] = 1,
    ACTIONS(46), 1,
      anon_sym_COLON,
  [139] = 1,
    ACTIONS(48), 1,
      ts_builtin_sym_end,
};

static const uint32_t ts_small_parse_table_map[] = {
  [SMALL_STATE(2)] = 0,
  [SMALL_STATE(3)] = 14,
  [SMALL_STATE(4)] = 28,
  [SMALL_STATE(5)] = 42,
  [SMALL_STATE(6)] = 55,
  [SMALL_STATE(7)] = 64,
  [SMALL_STATE(8)] = 73,
  [SMALL_STATE(9)] = 84,
  [SMALL_STATE(10)] = 93,
  [SMALL_STATE(11)] = 99,
  [SMALL_STATE(12)] = 106,
  [SMALL_STATE(13)] = 111,
  [SMALL_STATE(14)] = 115,
  [SMALL_STATE(15)] = 119,
  [SMALL_STATE(16)] = 123,
  [SMALL_STATE(17)] = 127,
  [SMALL_STATE(18)] = 131,
  [SMALL_STATE(19)] = 135,
  [SMALL_STATE(20)] = 139,
};

static const TSParseActionEntry ts_parse_actions[] = {
  [0] = {.entry = {.count = 0, .reusable = false}},
  [1] = {.entry = {.count = 1, .reusable = false}}, RECOVER(),
  [3] = {.entry = {.count = 1, .reusable = true}}, SHIFT(10),
  [5] = {.entry = {.count = 1, .reusable = false}}, SHIFT(6),
  [7] = {.entry = {.count = 1, .reusable = false}}, SHIFT(8),
  [9] = {.entry = {.count = 1, .reusable = true}}, SHIFT(13),
  [11] = {.entry = {.count = 1, .reusable = true}}, SHIFT(2),
  [13] = {.entry = {.count = 1, .reusable = true}}, SHIFT(14),
  [15] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_descr, 1, 0, 0),
  [17] = {.entry = {.count = 1, .reusable = false}}, REDUCE(aux_sym_descr_repeat1, 1, 0, 0),
  [19] = {.entry = {.count = 2, .reusable = false}}, REDUCE(aux_sym_descr_repeat1, 2, 0, 0), SHIFT_REPEAT(7),
  [22] = {.entry = {.count = 1, .reusable = false}}, SHIFT(9),
  [24] = {.entry = {.count = 1, .reusable = false}}, SHIFT(7),
  [26] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_descr, 2, 0, 0),
  [28] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_type, 1, 0, 0),
  [30] = {.entry = {.count = 1, .reusable = true}}, SHIFT(19),
  [32] = {.entry = {.count = 1, .reusable = true}}, SHIFT(3),
  [34] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_scope, 3, 0, 0),
  [36] = {.entry = {.count = 1, .reusable = true}}, SHIFT(16),
  [38] = {.entry = {.count = 1, .reusable = true}},  ACCEPT_INPUT(),
  [40] = {.entry = {.count = 1, .reusable = true}}, SHIFT(12),
  [42] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_hdr, 4, 0, 0),
  [44] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_hdr, 3, 0, 0),
  [46] = {.entry = {.count = 1, .reusable = true}}, SHIFT(4),
  [48] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_hdr, 5, 0, 0),
};

#ifdef __cplusplus
extern "C" {
#endif
#ifdef TREE_SITTER_HIDE_SYMBOLS
#define TS_PUBLIC
#elif defined(_WIN32)
#define TS_PUBLIC __declspec(dllexport)
#else
#define TS_PUBLIC __attribute__((visibility("default")))
#endif

TS_PUBLIC const TSLanguage *tree_sitter_git_msg(void) {
  static const TSLanguage language = {
    .version = LANGUAGE_VERSION,
    .symbol_count = SYMBOL_COUNT,
    .alias_count = ALIAS_COUNT,
    .token_count = TOKEN_COUNT,
    .external_token_count = EXTERNAL_TOKEN_COUNT,
    .state_count = STATE_COUNT,
    .large_state_count = LARGE_STATE_COUNT,
    .production_id_count = PRODUCTION_ID_COUNT,
    .field_count = FIELD_COUNT,
    .max_alias_sequence_length = MAX_ALIAS_SEQUENCE_LENGTH,
    .parse_table = &ts_parse_table[0][0],
    .small_parse_table = ts_small_parse_table,
    .small_parse_table_map = ts_small_parse_table_map,
    .parse_actions = ts_parse_actions,
    .symbol_names = ts_symbol_names,
    .symbol_metadata = ts_symbol_metadata,
    .public_symbol_map = ts_symbol_map,
    .alias_map = ts_non_terminal_alias_map,
    .alias_sequences = &ts_alias_sequences[0][0],
    .lex_modes = ts_lex_modes,
    .lex_fn = ts_lex,
    .primary_state_ids = ts_primary_state_ids,
  };
  return &language;
}
#ifdef __cplusplus
}
#endif
