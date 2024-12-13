/**
 * @file Parse git commit msgs
 * @author glencoe
 * @license MIT
 */

/// <reference types="tree-sitter-cli/dsl" />
// @ts-check

module.exports = grammar({
  name: "git_msg",

  rules: {
    hdr: $ => seq($.type, optional($.scope), optional('!'), ': ', $.summary),
    type: $ => $.word,
    word: $ => /[a-zA-Z0-9_-]+/,
    scope: $ => seq('(', $.word, ')'),
    symbol: $ => /[,:(){}/^_$; %+=!@#~><-]/,
    dot: $ => '.',
    summary: $ => seq(repeat(choice($.word, $.symbol, $.dot)), choice($.word, $.symbol)),
  }
});
