stdlib = """
.globl	insert_pubkey
.type	insert_pubkey, @function
CALL $insert_pubkey_macro$

.macro insert_pubkey_macro
.loc stdlib.sol, 14
SWAP
CTOS
.loc stdlib.sol, 15
NEWC
.loc stdlib.sol, 18
OVER
LDI 1
POP S3
PUSHCONT {
	.loc stdlib.sol, 19
	STSLICECONST 1
	.loc stdlib.sol, 20
	OVER
	LDU 32
	POP S3
	.loc stdlib.sol, 21
	SWAP
	STSLICECONST 1
	STU 32
}
PUSHCONT {
	.loc stdlib.sol, 23
	STSLICECONST 0
}
IFELSE
.loc stdlib.sol, 27
OVER
LDI 1
POP S3
PUSHCONT {
	.loc stdlib.sol, 28
	STSLICECONST 1
	.loc stdlib.sol, 29
	OVER
	LDI 1
	LDI 1
	POP S4
	.loc stdlib.sol, 30
	XCHG S2
	STI 1
	STI 1
}
PUSHCONT {
	.loc stdlib.sol, 32
	STSLICECONST 0
}
IFELSE
.loc stdlib.sol, 36
OVER
LDDICT
POP S3
SWAP
STDICT
.loc stdlib.sol, 40
NEWDICT
.loc stdlib.sol, 41
PUSH S2
LDI 1
POP S4
PUSHCONT {
	.loc stdlib.sol, 42
	PUSH S2
	LDREFRTOS
	SWAP
	POP S4
	.loc stdlib.sol, 43
	PLDDICT
	NIP
	.loc stdlib.sol, 0
}
IF
.loc stdlib.sol, 45
ROLL 3
PUSHINT 0
ROTREV
NEWC
STU 256
ROTREV
PUSHINT 64
DICTUSETB
.loc stdlib.sol, 47
NEWC
STDICT
.loc stdlib.sol, 48
OVER
STSLICECONST 1
POP S2
.loc stdlib.sol, 49
STBREFR
.loc stdlib.sol, 53
OVER
LDDICT
POP S3
SWAP
STDICT
.loc stdlib.sol, 55
SWAP
SEMPTY
THROWIFNOT 55
.loc stdlib.sol, 57
ENDC
.loc stdlib.sol, 0

.globl	replay_protection
.type	replay_protection, @function
CALL $replay_protection_macro$

.macro replay_protection_macro
.loc stdlib.sol, 61
GETGLOB 3
OVER
LESS
THROWIFNOT 52
.loc stdlib.sol, 62
DUP
NOW
PUSHINT 1000
MUL
PUSHINT 1800000
ADD
LESS
THROWIFNOT 52
.loc stdlib.sol, 63
SETGLOB 3
.loc stdlib.sol, 0

.globl	__tonToGas
.type	__tonToGas, @function
CALL $__tonToGas_macro$

.macro __tonToGas_macro
.loc stdlib.sol, 67
PUSHPOW2 16
SWAP
CALLREF {
	CALL $__gasGasPrice_macro$
}
MULDIV
.loc stdlib.sol, 0

.globl	__gasToTon
.type	__gasToTon, @function
CALL $__gasToTon_macro$

.macro __gasToTon_macro
.loc stdlib.sol, 71
CALLREF {
	CALL $__gasGasPrice_macro$
}
PUSHPOW2 16
MULDIVC
.loc stdlib.sol, 0

.globl	__gasGasPrice
.type	__gasGasPrice, @function
CALL $__gasGasPrice_macro$

.macro __gasGasPrice_macro
.loc stdlib.sol, 75
DUP
EQINT 0
OVER
EQINT -1
OR
THROWIFNOT 67
.loc stdlib.sol, 76
PUSHINT 20
PUSHINT 21
CONDSEL
CONFIGOPTPARAM
.loc stdlib.sol, 77
DUP
ISNULL
THROWIF 68
.loc stdlib.sol, 78
DUP
ISNULL
THROWIF 63
CTOS
.loc stdlib.sol, 79
LDU 8
LDU 64
LDU 64
LDU 8
PLDU 64
BLKDROP2 4, 1
.loc stdlib.sol, 0

.globl	__exp
.type	__exp, @function
CALL $__exp_macro$

.macro __exp_macro
.loc stdlib.sol, 83
PUSHINT 1
.loc stdlib.sol, 84
PUSHCONT {
	OVER
	NEQINT 0
}
PUSHCONT {
	.loc stdlib.sol, 85
	OVER
	MODPOW2 1
	PUSHCONT {
		.loc stdlib.sol, 86
		PUSH S2
		MUL
		.loc stdlib.sol, 87
		OVER
		DEC
	}
	PUSHCONT {
		.loc stdlib.sol, 89
		PUSH2 S2, S2
		MUL
		POP S3
		.loc stdlib.sol, 90
		OVER
		RSHIFT 1
	}
	IFELSE
	POP S2
	.loc stdlib.sol, 0
}
WHILE
.loc stdlib.sol, 93
BLKDROP2 2, 1
.loc stdlib.sol, 0

.globl	parseInteger
.type	parseInteger, @function
CALL $parseInteger_macro$

.macro parseInteger_macro
.loc stdlib.sol, 99
TUPLE 0
.loc stdlib.sol, 100
PUSH S2
PUSHCONT {
	.loc stdlib.sol, 101
	PUSHINT 0
	CALLREF {
		XCPU S1, S0
		TLEN
		PUSHCONT {
			TPOP
			DUP
			TLEN
			PUSHPOW2DEC 8
			SUB
			PUSHCONT {
				TPUSH
				TUPLE 0
			}
			IFNOT
		}
		PUSHCONT {
			TUPLE 0
		}
		IFELSE
		ROT
		TPUSH
		TPUSH
	}
	.loc stdlib.sol, 102
	BLKDROP2 2, 1
	.loc stdlib.sol, 0
}
IFNOTJMP
.loc stdlib.sol, 104
PUSHINT 0
.loc stdlib.sol, 105
PUSHCONT {
	PUSH S3
	NEQINT 0
}
PUSHCONT {
	.loc stdlib.sol, 106
	OVER2
	DIVMOD
	POP S2
	POP S4
	.loc stdlib.sol, 107
	DUP2
	CALLREF {
		XCPU S1, S0
		TLEN
		PUSHCONT {
			TPOP
			DUP
			TLEN
			PUSHPOW2DEC 8
			SUB
			PUSHCONT {
				TPUSH
				TUPLE 0
			}
			IFNOT
		}
		PUSHCONT {
			TUPLE 0
		}
		IFELSE
		ROT
		TPUSH
		TPUSH
	}
	POP S2
	.loc stdlib.sol, 0
}
WHILE
DROP
BLKDROP2 2, 1
.loc stdlib.sol, 0

.globl	convertIntToDecStr_short
.type	convertIntToDecStr_short, @function
CALL $convertIntToDecStr_short_macro$

.macro convertIntToDecStr_short_macro
.loc stdlib.sol, 112
ROTREV
PUSH S2
ABS
PUSHINT 0
DUP
ROLL 5
LESSINT 0
CALLREF {
	CALL $convertIntToDecStr_macro$
}
.loc stdlib.sol, 0

.globl	convertIntToDecStr
.type	convertIntToDecStr, @function
CALL $convertIntToDecStr_macro$

.macro convertIntToDecStr_macro
.loc stdlib.sol, 116
PUSH S4
BREMBITS
RSHIFT 3
.loc stdlib.sol, 117
DUP
PUSHCONT {
	.loc stdlib.sol, 118
	BLKPUSH 2, 6
	CALLREF {
		XCPU S1, S0
		TLEN
		PUSHCONT {
			TPOP
			DUP
			TLEN
			PUSHPOW2DEC 8
			SUB
			PUSHCONT {
				TPUSH
				TUPLE 0
			}
			IFNOT
		}
		PUSHCONT {
			TUPLE 0
		}
		IFELSE
		ROT
		TPUSH
		TPUSH
	}
	POP S7
	.loc stdlib.sol, 119
	NEWC
	POP S6
	.loc stdlib.sol, 120
	DROP
	PUSHINT 127
	.loc stdlib.sol, 0
}
IFNOT
.loc stdlib.sol, 122
ROT
PUSHINT 48
PUSHINT 32
CONDSEL
.loc stdlib.sol, 123
ROT
PUSHCONT {
	.loc stdlib.sol, 124
	PUSH S4
	STSLICECONST x2d
	POP S5
	.loc stdlib.sol, 0
}
IF
.loc stdlib.sol, 125
OVER
DEC
POP S2
.loc stdlib.sol, 126
OVER
PUSHCONT {
	.loc stdlib.sol, 127
	BLKPUSH 2, 5
	CALLREF {
		XCPU S1, S0
		TLEN
		PUSHCONT {
			TPOP
			DUP
			TLEN
			PUSHPOW2DEC 8
			SUB
			PUSHCONT {
				TPUSH
				TUPLE 0
			}
			IFNOT
		}
		PUSHCONT {
			TUPLE 0
		}
		IFELSE
		ROT
		TPUSH
		TPUSH
	}
	POP S6
	.loc stdlib.sol, 128
	NEWC
	POP S5
	.loc stdlib.sol, 129
	PUSHINT 127
	POP S2
	.loc stdlib.sol, 0
}
IFNOT
.loc stdlib.sol, 131
ROLL 3
PUSHINT 10
CALLREF {
	CALL $parseInteger_macro$
}
.loc stdlib.sol, 132
DUP
CALLREF {
	DUP
	TLEN
	DUP
	PUSHCONT {
		DEC
		PUSHPOW2DEC 8
		MUL
		SWAP
		LAST
		TLEN
		ADD
	}
	PUSHCONT {
		NIP
	}
	IFELSE
}
.loc stdlib.sol, 133
PUSH S4
PUSHCONT {
	.loc stdlib.sol, 134
	PUSH2 S4, S0
	LESS
	PUSH S5
	GTINT 127
	OR
	THROWIF 66
	.loc stdlib.sol, 136
	PUSH2 S4, S0
	SUB
	.loc stdlib.sol, 137
	PUSH2 S0, S4
	LEQ
	PUSHCONT {
		.loc stdlib.sol, 138
		DUP
		PUSHCONT {
			.loc stdlib.sol, 139
			PUSH2 S6, S3
			STUR 8
			POP S7
			.loc stdlib.sol, 0
		}
		REPEAT
		.loc stdlib.sol, 141
		PUSH2 S4, S0
		SUB
		POP S5
		.loc stdlib.sol, 142
		PUSH S4
		PUSHCONT {
			.loc stdlib.sol, 143
			BLKPUSH 2, 7
			CALLREF {
				XCPU S1, S0
				TLEN
				PUSHCONT {
					TPOP
					DUP
					TLEN
					PUSHPOW2DEC 8
					SUB
					PUSHCONT {
						TPUSH
						TUPLE 0
					}
					IFNOT
				}
				PUSHCONT {
					TUPLE 0
				}
				IFELSE
				ROT
				TPUSH
				TPUSH
			}
			POP S8
			.loc stdlib.sol, 144
			NEWC
			POP S7
			.loc stdlib.sol, 145
			PUSHINT 127
			POP S5
			.loc stdlib.sol, 0
		}
		IFNOT
	}
	PUSHCONT {
		.loc stdlib.sol, 148
		PUSH S4
		PUSHCONT {
			.loc stdlib.sol, 149
			PUSH2 S6, S3
			STUR 8
			POP S7
			.loc stdlib.sol, 0
		}
		REPEAT
		.loc stdlib.sol, 151
		BLKPUSH 2, 7
		CALLREF {
			XCPU S1, S0
			TLEN
			PUSHCONT {
				TPOP
				DUP
				TLEN
				PUSHPOW2DEC 8
				SUB
				PUSHCONT {
					TPUSH
					TUPLE 0
				}
				IFNOT
			}
			PUSHCONT {
				TUPLE 0
			}
			IFELSE
			ROT
			TPUSH
			TPUSH
		}
		POP S8
		.loc stdlib.sol, 152
		NEWC
		POP S7
		.loc stdlib.sol, 153
		PUSH2 S0, S4
		SUB
		PUSHCONT {
			.loc stdlib.sol, 154
			PUSH2 S6, S3
			STUR 8
			POP S7
			.loc stdlib.sol, 0
		}
		REPEAT
		.loc stdlib.sol, 156
		PUSHINT 127
		OVER
		SUB
		PUSH S5
		ADD
		POP S5
	}
	IFELSE
	.loc stdlib.sol, 0
	DROP
}
IF
.loc stdlib.sol, 159
PUSH2 S0, S3
LEQ
PUSHCONT {
	.loc stdlib.sol, 160
	DUP
	PUSHCONT {
		.loc stdlib.sol, 161
		OVER
		CALLREF {
			TPOP
			TPOP
			ROTREV
			DUP
			TLEN
			PUSHCONT {
				TPUSH
			}
			PUSHCONT {
				DROP
			}
			IFELSE
		}
		POP S3
		.loc stdlib.sol, 162
		PUSH S6
		PUSHINT 48
		ROT
		ADD
		STUR 8
		POP S6
		.loc stdlib.sol, 0
	}
	REPEAT
}
PUSHCONT {
	.loc stdlib.sol, 165
	PUSH S3
	PUSHCONT {
		.loc stdlib.sol, 166
		OVER
		CALLREF {
			TPOP
			TPOP
			ROTREV
			DUP
			TLEN
			PUSHCONT {
				TPUSH
			}
			PUSHCONT {
				DROP
			}
			IFELSE
		}
		POP S3
		.loc stdlib.sol, 167
		PUSH S6
		PUSHINT 48
		ROT
		ADD
		STUR 8
		POP S6
		.loc stdlib.sol, 0
	}
	REPEAT
	.loc stdlib.sol, 169
	BLKPUSH 2, 6
	CALLREF {
		XCPU S1, S0
		TLEN
		PUSHCONT {
			TPOP
			DUP
			TLEN
			PUSHPOW2DEC 8
			SUB
			PUSHCONT {
				TPUSH
				TUPLE 0
			}
			IFNOT
		}
		PUSHCONT {
			TUPLE 0
		}
		IFELSE
		ROT
		TPUSH
		TPUSH
	}
	POP S7
	.loc stdlib.sol, 170
	NEWC
	POP S6
	.loc stdlib.sol, 171
	PUSH2 S0, S3
	SUB
	PUSHCONT {
		.loc stdlib.sol, 172
		OVER
		CALLREF {
			TPOP
			TPOP
			ROTREV
			DUP
			TLEN
			PUSHCONT {
				TPUSH
			}
			PUSHCONT {
				DROP
			}
			IFELSE
		}
		POP S3
		.loc stdlib.sol, 173
		PUSH S6
		PUSHINT 48
		ROT
		ADD
		STUR 8
		POP S6
		.loc stdlib.sol, 0
	}
	REPEAT
}
IFELSE
.loc stdlib.sol, 177
BLKDROP 5
.loc stdlib.sol, 0

.globl	convertAddressToHexString
.type	convertAddressToHexString, @function
CALL $convertAddressToHexString_macro$

.macro convertAddressToHexString_macro
.loc stdlib.sol, 181
REWRITESTDADDR
.loc stdlib.sol, 182
OVER2
ROLL 3
CALLREF {
	CALL $convertIntToHexStr_short_macro$
}
POP S3
POP S3
.loc stdlib.sol, 183
OVER
BREMBITS
.loc stdlib.sol, 184
GTINT 8
PUSHCONT {
	.loc stdlib.sol, 187
	BLKPUSH 2, 2
	CALLREF {
		XCPU S1, S0
		TLEN
		PUSHCONT {
			TPOP
			DUP
			TLEN
			PUSHPOW2DEC 8
			SUB
			PUSHCONT {
				TPUSH
				TUPLE 0
			}
			IFNOT
		}
		PUSHCONT {
			TUPLE 0
		}
		IFELSE
		ROT
		TPUSH
		TPUSH
	}
	POP S3
	.loc stdlib.sol, 188
	NEWC
	POP S2
	.loc stdlib.sol, 189
}
IFNOT
OVER
STSLICECONST x3a
POP S2
.loc stdlib.sol, 191
PUSHINT 64
TRUE
DUP
FALSE
CALLREF {
	CALL $convertIntToHexStr_macro$
}
.loc stdlib.sol, 0

.globl	convertFixedPointToString
.type	convertFixedPointToString, @function
CALL $convertFixedPointToString_macro$

.macro convertFixedPointToString_macro
.loc stdlib.sol, 195
OVER
ABS
.loc stdlib.sol, 196
PUSHINT 10
PUSH3 S2, S0, S2
OR
THROWIFNOT 69
CALLREF {
	CALL $__exp_macro$
}
DIVMOD
.loc stdlib.sol, 197
BLKPUSH 2, 5
ROLL 3
PUSHINT 0
DUP
ROLL 7
SGN
LESSINT 0
CALLREF {
	CALL $convertIntToDecStr_macro$
}
POP S4
POP S4
.loc stdlib.sol, 198
PUSH S2
BREMBITS
.loc stdlib.sol, 199
GTINT 8
PUSHCONT {
	.loc stdlib.sol, 202
	OVER2
	CALLREF {
		XCPU S1, S0
		TLEN
		PUSHCONT {
			TPOP
			DUP
			TLEN
			PUSHPOW2DEC 8
			SUB
			PUSHCONT {
				TPUSH
				TUPLE 0
			}
			IFNOT
		}
		PUSHCONT {
			TUPLE 0
		}
		IFELSE
		ROT
		TPUSH
		TPUSH
	}
	POP S4
	.loc stdlib.sol, 203
	NEWC
	POP S3
	.loc stdlib.sol, 204
}
IFNOT
PUSH S2
STSLICECONST x2e
POP S3
.loc stdlib.sol, 206
SWAP
TRUE
FALSE
CALLREF {
	CALL $convertIntToDecStr_macro$
}
.loc stdlib.sol, 0

.globl	convertIntToHexStr_short
.type	convertIntToHexStr_short, @function
CALL $convertIntToHexStr_short_macro$

.macro convertIntToHexStr_short_macro
.loc stdlib.sol, 210
ROTREV
PUSH S2
ABS
PUSHINT 0
DUP
TRUE
ROLL 6
LESSINT 0
CALLREF {
	CALL $convertIntToHexStr_macro$
}
.loc stdlib.sol, 0

.globl	convertIntToHexStr
.type	convertIntToHexStr, @function
CALL $convertIntToHexStr_macro$

.macro convertIntToHexStr_macro
.loc stdlib.sol, 214
PUSH S5
BREMBITS
RSHIFT 3
.loc stdlib.sol, 215
DUP
PUSHCONT {
	.loc stdlib.sol, 216
	BLKPUSH 2, 7
	CALLREF {
		XCPU S1, S0
		TLEN
		PUSHCONT {
			TPOP
			DUP
			TLEN
			PUSHPOW2DEC 8
			SUB
			PUSHCONT {
				TPUSH
				TUPLE 0
			}
			IFNOT
		}
		PUSHCONT {
			TUPLE 0
		}
		IFELSE
		ROT
		TPUSH
		TPUSH
	}
	POP S8
	.loc stdlib.sol, 217
	NEWC
	POP S7
	.loc stdlib.sol, 218
	DROP
	PUSHINT 127
	.loc stdlib.sol, 0
}
IFNOT
.loc stdlib.sol, 220
ROLL 3
PUSHINT 48
PUSHINT 32
CONDSEL
.loc stdlib.sol, 221
ROT
PUSHCONT {
	.loc stdlib.sol, 222
	PUSH S5
	STSLICECONST x2d
	POP S6
	.loc stdlib.sol, 0
}
IF
.loc stdlib.sol, 223
OVER
DEC
POP S2
.loc stdlib.sol, 224
OVER
PUSHCONT {
	.loc stdlib.sol, 225
	BLKPUSH 2, 6
	CALLREF {
		XCPU S1, S0
		TLEN
		PUSHCONT {
			TPOP
			DUP
			TLEN
			PUSHPOW2DEC 8
			SUB
			PUSHCONT {
				TPUSH
				TUPLE 0
			}
			IFNOT
		}
		PUSHCONT {
			TUPLE 0
		}
		IFELSE
		ROT
		TPUSH
		TPUSH
	}
	POP S7
	.loc stdlib.sol, 226
	NEWC
	POP S6
	.loc stdlib.sol, 227
	PUSHINT 127
	POP S2
	.loc stdlib.sol, 0
}
IFNOT
.loc stdlib.sol, 229
ROLL 4
PUSHINT 16
CALLREF {
	CALL $parseInteger_macro$
}
.loc stdlib.sol, 230
DUP
CALLREF {
	DUP
	TLEN
	DUP
	PUSHCONT {
		DEC
		PUSHPOW2DEC 8
		MUL
		SWAP
		LAST
		TLEN
		ADD
	}
	PUSHCONT {
		NIP
	}
	IFELSE
}
.loc stdlib.sol, 232
PUSH S5
PUSHCONT {
	.loc stdlib.sol, 233
	PUSH2 S5, S0
	LESS
	PUSH S6
	GTINT 127
	OR
	THROWIF 69
	.loc stdlib.sol, 235
	PUSH2 S5, S0
	SUB
	.loc stdlib.sol, 236
	PUSH2 S0, S4
	LEQ
	PUSHCONT {
		.loc stdlib.sol, 237
		DUP
		PUSHCONT {
			.loc stdlib.sol, 238
			PUSH2 S7, S3
			STUR 8
			POP S8
			.loc stdlib.sol, 0
		}
		REPEAT
		.loc stdlib.sol, 240
		PUSH2 S4, S0
		SUB
		POP S5
		.loc stdlib.sol, 241
		PUSH S4
		PUSHCONT {
			.loc stdlib.sol, 242
			BLKPUSH 2, 8
			CALLREF {
				XCPU S1, S0
				TLEN
				PUSHCONT {
					TPOP
					DUP
					TLEN
					PUSHPOW2DEC 8
					SUB
					PUSHCONT {
						TPUSH
						TUPLE 0
					}
					IFNOT
				}
				PUSHCONT {
					TUPLE 0
				}
				IFELSE
				ROT
				TPUSH
				TPUSH
			}
			POP S9
			.loc stdlib.sol, 243
			NEWC
			POP S8
			.loc stdlib.sol, 244
			PUSHINT 127
			POP S5
			.loc stdlib.sol, 0
		}
		IFNOT
	}
	PUSHCONT {
		.loc stdlib.sol, 247
		PUSH S4
		PUSHCONT {
			.loc stdlib.sol, 248
			PUSH2 S7, S3
			STUR 8
			POP S8
			.loc stdlib.sol, 0
		}
		REPEAT
		.loc stdlib.sol, 250
		BLKPUSH 2, 8
		CALLREF {
			XCPU S1, S0
			TLEN
			PUSHCONT {
				TPOP
				DUP
				TLEN
				PUSHPOW2DEC 8
				SUB
				PUSHCONT {
					TPUSH
					TUPLE 0
				}
				IFNOT
			}
			PUSHCONT {
				TUPLE 0
			}
			IFELSE
			ROT
			TPUSH
			TPUSH
		}
		POP S9
		.loc stdlib.sol, 251
		NEWC
		POP S8
		.loc stdlib.sol, 252
		PUSH2 S0, S4
		SUB
		PUSHCONT {
			.loc stdlib.sol, 253
			PUSH2 S7, S3
			STUR 8
			POP S8
			.loc stdlib.sol, 0
		}
		REPEAT
		.loc stdlib.sol, 255
		PUSHINT 127
		OVER
		SUB
		PUSH S5
		ADD
		POP S5
	}
	IFELSE
	.loc stdlib.sol, 0
	DROP
}
IF
.loc stdlib.sol, 258
PUSH2 S0, S3
LEQ
PUSHCONT {
	.loc stdlib.sol, 259
	DUP
	PUSHCONT {
		.loc stdlib.sol, 260
		OVER
		CALLREF {
			TPOP
			TPOP
			ROTREV
			DUP
			TLEN
			PUSHCONT {
				TPUSH
			}
			PUSHCONT {
				DROP
			}
			IFELSE
		}
		POP S3
		.loc stdlib.sol, 261
		DUP
		LESSINT 10
		PUSHCONT {
			.loc stdlib.sol, 262
			PUSH S7
			PUSHINT 48
		}
		PUSHCONT {
			.loc stdlib.sol, 264
			PUSH2 S7, S5
			PUSHINT 87
			PUSHINT 55
			CONDSEL
		}
		IFELSE
		PUSH S2
		ADD
		STUR 8
		POP S8
		.loc stdlib.sol, 0
		DROP
	}
	REPEAT
}
PUSHCONT {
	.loc stdlib.sol, 267
	PUSH S3
	PUSHCONT {
		.loc stdlib.sol, 268
		OVER
		CALLREF {
			TPOP
			TPOP
			ROTREV
			DUP
			TLEN
			PUSHCONT {
				TPUSH
			}
			PUSHCONT {
				DROP
			}
			IFELSE
		}
		POP S3
		.loc stdlib.sol, 269
		DUP
		LESSINT 10
		PUSHCONT {
			.loc stdlib.sol, 270
			PUSH S7
			PUSHINT 48
		}
		PUSHCONT {
			.loc stdlib.sol, 272
			PUSH2 S7, S5
			PUSHINT 87
			PUSHINT 55
			CONDSEL
		}
		IFELSE
		PUSH S2
		ADD
		STUR 8
		POP S8
		.loc stdlib.sol, 0
		DROP
	}
	REPEAT
	.loc stdlib.sol, 274
	BLKPUSH 2, 7
	CALLREF {
		XCPU S1, S0
		TLEN
		PUSHCONT {
			TPOP
			DUP
			TLEN
			PUSHPOW2DEC 8
			SUB
			PUSHCONT {
				TPUSH
				TUPLE 0
			}
			IFNOT
		}
		PUSHCONT {
			TUPLE 0
		}
		IFELSE
		ROT
		TPUSH
		TPUSH
	}
	POP S8
	.loc stdlib.sol, 275
	NEWC
	POP S7
	.loc stdlib.sol, 276
	PUSH2 S0, S3
	SUB
	PUSHCONT {
		.loc stdlib.sol, 277
		OVER
		CALLREF {
			TPOP
			TPOP
			ROTREV
			DUP
			TLEN
			PUSHCONT {
				TPUSH
			}
			PUSHCONT {
				DROP
			}
			IFELSE
		}
		POP S3
		.loc stdlib.sol, 278
		DUP
		LESSINT 10
		PUSHCONT {
			.loc stdlib.sol, 279
			PUSH S7
			PUSHINT 48
		}
		PUSHCONT {
			.loc stdlib.sol, 281
			PUSH2 S7, S5
			PUSHINT 87
			PUSHINT 55
			CONDSEL
		}
		IFELSE
		PUSH S2
		ADD
		STUR 8
		POP S8
		.loc stdlib.sol, 0
		DROP
	}
	REPEAT
}
IFELSE
.loc stdlib.sol, 284
BLKDROP 6
.loc stdlib.sol, 0

.globl	storeStringInBuilders
.type	storeStringInBuilders, @function
CALL $storeStringInBuilders_macro$

.macro storeStringInBuilders_macro
.loc stdlib.sol, 288
OVER
BREMBITS
ADDCONST -7
.loc stdlib.sol, 289
OVER
SBITREFS
.loc stdlib.sol, 290
DUP
PUSHCONT {
	.loc stdlib.sol, 291
	PUSH S3
	PUSHINT 0
	PUSH S2
	SSKIPFIRST
	POP S4
	.loc stdlib.sol, 0
}
IF
.loc stdlib.sol, 292
DROP
OVER
LEQ
.loc stdlib.sol, 293
PUSHCONT {
	.loc stdlib.sol, 296
	DUP2
	LDSLICEX
	POP S3
	.loc stdlib.sol, 297
	PUSH S3
	STSLICE
	POP S3
	.loc stdlib.sol, 298
	OVER2
	CALLREF {
		XCPU S1, S0
		TLEN
		PUSHCONT {
			TPOP
			DUP
			TLEN
			PUSHPOW2DEC 8
			SUB
			PUSHCONT {
				TPUSH
				TUPLE 0
			}
			IFNOT
		}
		PUSHCONT {
			TUPLE 0
		}
		IFELSE
		ROT
		TPUSH
		TPUSH
	}
	POP S4
	.loc stdlib.sol, 299
	NEWC
	POP S3
	.loc stdlib.sol, 300
}
IFNOT
PUSH2 S1, S2
STSLICE
BLKDROP2 3, 1
.loc stdlib.sol, 0

.globl	assembleList
.type	assembleList, @function
CALL $assembleList_macro$

.macro assembleList_macro
.loc stdlib.sol, 306
PUSHCONT {
	OVER
	TLEN
	ISZERO
	NOT
}
PUSHCONT {
	.loc stdlib.sol, 307
	OVER
	CALLREF {
		TPOP
		TPOP
		ROTREV
		DUP
		TLEN
		PUSHCONT {
			TPUSH
		}
		PUSHCONT {
			DROP
		}
		IFELSE
	}
	POP S3
	.loc stdlib.sol, 308
	STBREF
	.loc stdlib.sol, 0
}
WHILE
.loc stdlib.sol, 311
ENDC
NIP
.loc stdlib.sol, 0

.globl	__stoi
.type	__stoi, @function
CALL $__stoi_macro$

.macro __stoi_macro
.loc stdlib.sol, 315
CTOS
.loc stdlib.sol, 316
DUP
SBITS
LESSINT 8
PUSHCONT {
	.loc stdlib.sol, 317
	DROP
	NULL
	.loc stdlib.sol, 0
}
IFJMP
.loc stdlib.sol, 319
BLKPUSH 2, 0
.loc stdlib.sol, 320
LDU 8
POP S2
.loc stdlib.sol, 321
DUP
EQINT 45
.loc stdlib.sol, 322
PUSHINT 0
.loc stdlib.sol, 323
PUSH S3
SBITS
.loc stdlib.sol, 324
PUSH2 S2, S0
GTINT 15
AND
PUSHCONT {
	.loc stdlib.sol, 325
	PUSH S4
	LDU 8
	LDU 8
	POP S7
	POP S3
	POP S4
	.loc stdlib.sol, 0
}
IF
.loc stdlib.sol, 327
PUSH S2
NOT
SWAP
GTINT 7
AND
PUSHCONT {
	.loc stdlib.sol, 328
	PUSH S3
	LDU 8
	POP S5
	NIP
	.loc stdlib.sol, 0
}
IF
.loc stdlib.sol, 330
ROT
EQINT 48
SWAP
EQINT 120
AND
.loc stdlib.sol, 332
OVER
PUSHCONT {
	.loc stdlib.sol, 333
	PUSH S3
	LDU 8
	NIP
	POP S4
	.loc stdlib.sol, 0
}
IF
.loc stdlib.sol, 334
DUP
PUSHCONT {
	.loc stdlib.sol, 335
	PUSH S3
	LDU 8
	LDU 8
	BLKDROP2 2, 1
	POP S4
	.loc stdlib.sol, 0
}
IF
.loc stdlib.sol, 337
PUSHINT 0
.loc stdlib.sol, 339
PUSH S4
SBITS
RSHIFT 3
.loc stdlib.sol, 341
FALSE ; decl return flag
ROLL 3
PUSHCONT {
	.loc stdlib.sol, 342
	FALSE ; decl return flag
	PUSH S2
	PUSHCONT {
		.loc stdlib.sol, 343
		PUSH S6
		LDU 8
		POP S8
		.loc stdlib.sol, 344
		PUSH S4
		MULCONST 16
		POP S5
		.loc stdlib.sol, 345
		DUP
		GTINT 47
		OVER
		LESSINT 58
		AND
		PUSHCONT {
			.loc stdlib.sol, 346
			DUP
			ADDCONST -48
			PUSH S5
			ADD
			POP S5
			.loc stdlib.sol, 0
		}
		PUSHCONT {
			DUP
			GTINT 64
			OVER
			LESSINT 71
			AND
			PUSHCONT {
				.loc stdlib.sol, 348
				DUP
				ADDCONST -55
				PUSH S5
				ADD
				POP S5
				.loc stdlib.sol, 0
			}
			PUSHCONT {
				DUP
				GTINT 96
				OVER
				LESSINT 103
				AND
				PUSHCONT {
					.loc stdlib.sol, 350
					DUP
					ADDCONST -87
					PUSH S5
					ADD
					POP S5
					.loc stdlib.sol, 0
				}
				PUSHCONT {
					.loc stdlib.sol, 352
					BLKDROP 8
					NULL
					PUSHINT 4
					RETALT
					.loc stdlib.sol, 0
				}
				IFELSE
			}
			IFELSE
		}
		IFELSE
		DROP
		.loc stdlib.sol, 0
	}
	REPEATBRK
	DUP
	IFRET
	DROP
	.loc stdlib.sol, 0
}
PUSHCONT {
	.loc stdlib.sol, 356
	FALSE ; decl return flag
	PUSH S2
	PUSHCONT {
		.loc stdlib.sol, 357
		PUSH S6
		LDU 8
		POP S8
		.loc stdlib.sol, 358
		DUP
		LESSINT 48
		OVER
		GTINT 57
		OR
		PUSHCONT {
			BLKDROP 8
			NULL
			PUSHINT 4
			RETALT
		}
		IFJMP
		.loc stdlib.sol, 360
		PUSH S4
		MULCONST 10
		POP S5
		.loc stdlib.sol, 361
		ADDCONST -48
		PUSH S4
		ADD
		POP S4
		.loc stdlib.sol, 0
	}
	REPEATBRK
	DUP
	IFRET
	DROP
	.loc stdlib.sol, 0
}
IFELSE
IFRET
.loc stdlib.sol, 364
DROP
SWAP
PUSHCONT {
	.loc stdlib.sol, 365
	NEGATE
	.loc stdlib.sol, 0
}
IF
.loc stdlib.sol, 366
BLKDROP2 2, 1
.loc stdlib.sol, 0

.globl	strToList
.type	strToList, @function
CALL $strToList_macro$

.macro strToList_macro
.loc stdlib.sol, 370
TUPLE 0
.loc stdlib.sol, 371
SWAP
CTOS
.loc stdlib.sol, 372
PUSHCONT {
	DUP
	SREFS
	NEQINT 0
}
PUSHCONT {
	.loc stdlib.sol, 373
	LDREFRTOS
	.loc stdlib.sol, 375
	SWAP
	NEWC
	STSLICE
	.loc stdlib.sol, 376
	PUXC S2, S-1
	CALLREF {
		XCPU S1, S0
		TLEN
		PUSHCONT {
			TPOP
			DUP
			TLEN
			PUSHPOW2DEC 8
			SUB
			PUSHCONT {
				TPUSH
				TUPLE 0
			}
			IFNOT
		}
		PUSHCONT {
			TUPLE 0
		}
		IFELSE
		ROT
		TPUSH
		TPUSH
	}
	POP S2
	.loc stdlib.sol, 0
}
WHILE
.loc stdlib.sol, 380
NEWC
STSLICE
.loc stdlib.sol, 0

.globl	bytes_substr
.type	bytes_substr, @function
CALL $bytes_substr_macro$

.macro bytes_substr_macro
.loc stdlib.sol, 385
PUSH S3
PUSHPOW2DEC 32
CDATASIZE
DROP
NIP
.loc stdlib.sol, 386
RSHIFT 3
.loc stdlib.sol, 387
SWAP
PUSHCONT {
	.loc stdlib.sol, 388
	DUP
	POP S2
	.loc stdlib.sol, 0
}
IF
.loc stdlib.sol, 389
PUSH2 S1, S2
GEQ
THROWIFNOT 70
.loc stdlib.sol, 390
XCPU S1, S2
SUB
.loc stdlib.sol, 391
SWAP
BLKPUSH 2, 2
ADD
GEQ
THROWIFNOT 70
.loc stdlib.sol, 392
CALLREF {
	CALL $__subCell_macro$
}
.loc stdlib.sol, 0

.globl	__substr
.type	__substr, @function
CALL $__substr_macro$

.macro __substr_macro
.loc stdlib.sol, 396
PUSH S2
PUSHPOW2DEC 32
CDATASIZE
DROP
NIP
.loc stdlib.sol, 397
RSHIFT 3
.loc stdlib.sol, 398
OVER
EQINT -1
PUSHCONT {
	.loc stdlib.sol, 399
	PUSH2 S0, S2
	SUB
	FITS 256
	POP S2
	.loc stdlib.sol, 0
}
IF
.loc stdlib.sol, 400
BLKPUSH 2, 2
UFITS 256
ADD
GEQ
THROWIFNOT 70
.loc stdlib.sol, 401
UFITS 256
CALLREF {
	CALL $__subCell_macro$
}
.loc stdlib.sol, 0

.globl	__subCell
.type	__subCell, @function
CALL $__subCell_macro$

.macro __subCell_macro
.loc stdlib.sol, 404
PUSHREF {
}
.loc stdlib.sol, 405
OVER
PUSHCONT {
	.loc stdlib.sol, 406
	BLKDROP2 3, 1
	.loc stdlib.sol, 0
}
IFNOTJMP
.loc stdlib.sol, 408
DROP
SWAP
PUSHINT 127
DIVMOD
.loc stdlib.sol, 409
ROLL 3
CTOS
.loc stdlib.sol, 410
ROT
PUSHCONT {
	.loc stdlib.sol, 411
	LDREFRTOS
	NIP
	.loc stdlib.sol, 0
}
REPEAT
.loc stdlib.sol, 413
SWAP
MULCONST 8
SDSKIPFIRST
.loc stdlib.sol, 414
TUPLE 0
.loc stdlib.sol, 415
NEWC
.loc stdlib.sol, 416
PUSHCONT {
	PUSH S3
	NEQINT 0
}
PUSHCONT {
	.loc stdlib.sol, 417
	OVER2
	SBITS
	RSHIFT 3
	PUSH S2
	BREMBITS
	RSHIFT 3
	MIN
	MIN
	.loc stdlib.sol, 418
	PUSH3 S1, S3, S0
	LSHIFT 3
	UFITS 16
	LDSLICEX
	POP S6
	STSLICER
	POP S2
	.loc stdlib.sol, 419
	PUSH S4
	SUBR
	POP S4
	.loc stdlib.sol, 420
	PUSH S3
	PUSHCONT {
		.loc stdlib.sol, 421
		PUSH S2
		SBITS
		PUSHCONT {
			.loc stdlib.sol, 422
			PUSH S2
			LDREFRTOS
			NIP
			POP S3
			.loc stdlib.sol, 0
		}
		IFNOT
		.loc stdlib.sol, 424
		DUP
		BREMBITS
		LESSINT 8
		PUSHCONT {
			.loc stdlib.sol, 425
			CALLREF {
				XCPU S1, S0
				TLEN
				PUSHCONT {
					TPOP
					DUP
					TLEN
					PUSHPOW2DEC 8
					SUB
					PUSHCONT {
						TPUSH
						TUPLE 0
					}
					IFNOT
				}
				PUSHCONT {
					TUPLE 0
				}
				IFELSE
				ROT
				TPUSH
				TPUSH
			}
			.loc stdlib.sol, 426
			NEWC
			.loc stdlib.sol, 0
		}
		IF
		.loc stdlib.sol, 0
	}
	IF
	.loc stdlib.sol, 0
}
WHILE
.loc stdlib.sol, 430
CALLREF {
	CALL $assembleList_macro$
}
BLKDROP2 2, 1
.loc stdlib.sol, 0

.globl	compareLongStrings
.type	compareLongStrings, @function
CALL $compareLongStrings_macro$

.macro compareLongStrings_macro
.loc stdlib.sol, 437
SWAP
CTOS
.loc stdlib.sol, 438
SWAP
CTOS
.loc stdlib.sol, 439
FALSE ; decl return flag
PUSHCONT {
	.loc stdlib.sol, 440
	BLKPUSH 2, 2
	SDLEXCMP
	.loc stdlib.sol, 441
	DUP
	PUSHCONT {
		.loc stdlib.sol, 442
		BLKDROP2 3, 1
		PUSHINT 4
		RETALT
		.loc stdlib.sol, 0
	}
	IFJMP
	.loc stdlib.sol, 444
	DROP
	PUSH S2
	SREFS
	.loc stdlib.sol, 445
	PUSH S2
	SREFS
	.loc stdlib.sol, 446
	DUP2
	GREATER
	PUSHCONT {
		BLKDROP 5
		PUSHINT 1
		PUSHINT 4
		RETALT
	}
	IFJMP
	.loc stdlib.sol, 448
	PUSH2 S0, S1
	GREATER
	PUSHCONT {
		BLKDROP 5
		PUSHINT -1
		PUSHINT 4
		RETALT
	}
	IFJMP
	.loc stdlib.sol, 450
	ADD
	PUSHCONT {
		BLKDROP 3
		PUSHINT 0
		PUSHINT 4
		RETALT
	}
	IFNOTJMP
	.loc stdlib.sol, 452
	PUSH S2
	LDREFRTOS
	NIP
	POP S3
	.loc stdlib.sol, 453
	OVER
	LDREFRTOS
	NIP
	POP S2
	.loc stdlib.sol, 0
}
AGAINBRK
IFRET
.loc stdlib.sol, 455
DROP2
PUSHINT 0
.loc stdlib.sol, 0

.globl	concatenateStrings
.type	concatenateStrings, @function
CALL $concatenateStrings_macro$

.macro concatenateStrings_macro
.loc stdlib.sol, 459
SWAP
CALLREF {
	CALL $strToList_macro$
}
.loc stdlib.sol, 460
ROT
CTOS
.loc stdlib.sol, 461
BLKPUSH 3, 2
CALLREF {
	CALL $storeStringInBuilders_macro$
}
POP S3
POP S3
.loc stdlib.sol, 462
PUSHCONT {
	DUP
	PUSHINT 1
	SCHKREFSQ
}
PUSHCONT {
	.loc stdlib.sol, 463
	LDREFRTOS
	NIP
	.loc stdlib.sol, 464
	BLKPUSH 3, 2
	CALLREF {
		CALL $storeStringInBuilders_macro$
	}
	POP S3
	POP S3
	.loc stdlib.sol, 0
}
WHILE
.loc stdlib.sol, 466
DROP
CALLREF {
	CALL $assembleList_macro$
}
.loc stdlib.sol, 0

.globl	__strchr
.type	__strchr, @function
CALL $__strchr_macro$

.macro __strchr_macro
.loc stdlib.sol, 469
NULL
.loc stdlib.sol, 470
PUSHINT 0
.loc stdlib.sol, 471
ROLL 3
CTOS
NULL
FALSE ; decl return flag
PUSHCONT {
	PUSH S2
	SEMPTY
	NOT
}
PUSHCONT {
	PUSH S2
	LDUQ 8
	PUSHCONT {
		PLDREF
		CTOS
		LDU 8
	}
	IFNOT
	POP S4
	POP S2
	.loc stdlib.sol, 472
	PUSH2 S1, S5
	EQUAL
	PUSHCONT {
		.loc stdlib.sol, 473
		ROLL 3
		BLKDROP2 5, 1
		PUSHINT 4
		RETALT
		.loc stdlib.sol, 0
	}
	IFJMP
	.loc stdlib.sol, 475
	PUSH S3
	INC
	POP S4
	.loc stdlib.sol, 0
}
WHILEBRK
IFRET
BLKDROP 3
NIP
.loc stdlib.sol, 0

.globl	__strrchr
.type	__strrchr, @function
CALL $__strrchr_macro$

.macro __strrchr_macro
.loc stdlib.sol, 479
NULL
.loc stdlib.sol, 480
PUSHINT 0
.loc stdlib.sol, 481
ROLL 3
CTOS
NULL
PUSHCONT {
	OVER
	SEMPTY
	NOT
}
PUSHCONT {
	OVER
	LDUQ 8
	PUSHCONT {
		PLDREF
		CTOS
		LDU 8
	}
	IFNOT
	POP S3
	NIP
	.loc stdlib.sol, 482
	PUSH2 S0, S4
	EQUAL
	PUSHCONT {
		.loc stdlib.sol, 483
		PUSH S2
		POP S4
		.loc stdlib.sol, 0
	}
	IF
	.loc stdlib.sol, 485
	PUSH S2
	INC
	POP S3
	.loc stdlib.sol, 0
}
WHILE
BLKDROP 3
NIP
.loc stdlib.sol, 0

.globl	__strstr
.type	__strstr, @function
CALL $__strstr_macro$

.macro __strstr_macro
.loc stdlib.sol, 514
NULL
.loc stdlib.sol, 515
PUSH S2
CTOS
.loc stdlib.sol, 516
PUSH S2
CTOS
.loc stdlib.sol, 517
DUP
PUSHPOW2DEC 32
SDATASIZE
DROP
NIP
.loc stdlib.sol, 518
PUSH S2
PUSHPOW2DEC 32
SDATASIZE
DROP
NIP
.loc stdlib.sol, 519
DUP2
GREATER
PUSHCONT {
	.loc stdlib.sol, 520
	ROLL 4
	BLKDROP2 6, 1
	.loc stdlib.sol, 0
}
IFJMP
.loc stdlib.sol, 522
OVER
RSHIFT 3
POP S2
.loc stdlib.sol, 523
RSHIFT 3
.loc stdlib.sol, 524
PUSH2 S0, S2
.loc stdlib.sol, 525
LDU 8
POP S5
.loc stdlib.sol, 526
FALSE ; decl return flag
PUSHCONT {
	PUSH2 S3, S4
	GEQ
}
PUSHCONT {
	.loc stdlib.sol, 527
	PUSH S6
	LDU 8
	POP S8
	.loc stdlib.sol, 528
	PUSH S7
	SBITREFS
	.loc stdlib.sol, 529
	OVER
	LESSINT 8
	OVER
	GTINT 0
	AND
	PUSHCONT {
		.loc stdlib.sol, 530
		PUSH S9
		LDREFRTOS
		NIP
		POP S10
		.loc stdlib.sol, 0
	}
	IF
	.loc stdlib.sol, 532
	PUSH2 S2, S4
	EQUAL
	PUSHCONT {
		.loc stdlib.sol, 533
		BLKPUSH 2, 9
		PUSHCONT {
			.loc stdlib.sol, 491
			OVER
			SBITS
			.loc stdlib.sol, 492
			OVER
			SBITS
			.loc stdlib.sol, 493
			FALSE ; decl return flag
			PUSHCONT {
				PUSH S2
				NEQINT 0
				PUSH S2
				NEQINT 0
				AND
			}
			PUSHCONT {
				.loc stdlib.sol, 494
				BLKPUSH 2, 2
				MIN
				.loc stdlib.sol, 495
				PUSH2 S5, S0
				LDSLICEX
				POP S7
				.loc stdlib.sol, 496
				PUSH2 S5, S1
				LDSLICEX
				POP S7
				.loc stdlib.sol, 497
				PUSH2 S5, S2
				SUB
				POP S6
				.loc stdlib.sol, 498
				ROT
				PUSH S4
				SUBR
				POP S4
				.loc stdlib.sol, 499
				SDEQ
				PUSHCONT {
					.loc stdlib.sol, 500
					BLKDROP 5
					FALSE
					PUSHINT 4
					RETALT
					.loc stdlib.sol, 0
				}
				IFNOTJMP
				.loc stdlib.sol, 502
				PUSH S2
				EQINT 0
				PUSH S5
				SREFS
				NEQINT 0
				AND
				PUSHCONT {
					.loc stdlib.sol, 503
					PUSH S4
					LDREFRTOS
					NIP
					POP S5
					.loc stdlib.sol, 504
					PUSH S4
					SBITS
					POP S3
					.loc stdlib.sol, 0
				}
				IF
				.loc stdlib.sol, 506
				OVER
				EQINT 0
				PUSH S4
				SREFS
				NEQINT 0
				AND
				PUSHCONT {
					.loc stdlib.sol, 507
					PUSH S3
					LDREFRTOS
					NIP
					POP S4
					.loc stdlib.sol, 508
					PUSH S3
					SBITS
					POP S2
					.loc stdlib.sol, 0
				}
				IF
				.loc stdlib.sol, 0
			}
			WHILEBRK
			IFRET
			.loc stdlib.sol, 511
			BLKDROP 4
			TRUE
			.loc stdlib.sol, 490
		}
		CALLX
		.loc stdlib.sol, 0
		PUSHCONT {
			.loc stdlib.sol, 534
			BLKSWAP 2, 5
			SUBR
			UFITS 32
			POP S9
			.loc stdlib.sol, 535
			ROLL 8
			BLKDROP2 10, 1
			PUSHINT 4
			RETALT
			.loc stdlib.sol, 0
		}
		IFJMP
	}
	IF
	.loc stdlib.sol, 538
	BLKDROP 3
	PUSH S3
	DEC
	POP S4
	.loc stdlib.sol, 0
}
WHILEBRK
IFRET
.loc stdlib.sol, 540
BLKDROP 6
BLKDROP2 2, 1
.loc stdlib.sol, 0

.globl	__toLowerCase
.type	__toLowerCase, @function
CALL $__toLowerCase_macro$

.macro __toLowerCase_macro
.loc stdlib.sol, 549
NEWC
NULL
PAIR
.loc stdlib.sol, 550
PUSHINT 0
.loc stdlib.sol, 551
ROT
CTOS
NULL
PUSHCONT {
	OVER
	SEMPTY
	NOT
}
PUSHCONT {
	OVER
	LDUQ 8
	PUSHCONT {
		PLDREF
		CTOS
		LDU 8
	}
	IFNOT
	POP S3
	NIP
	.loc stdlib.sol, 552
	BLKPUSH 2, 0
	.loc stdlib.sol, 553
	GTINT 64
	OVER
	LESSINT 91
	AND
	PUSHCONT {
		.loc stdlib.sol, 554
		ADDCONST 32
		.loc stdlib.sol, 0
	}
	IF
	.loc stdlib.sol, 556
	PUSH2 S4, S4
	FIRST
	XCHG S1, S2
	STU 8
	SETINDEX 0
	POP S4
	.loc stdlib.sol, 557
	PUSH S2
	INC
	POP S3
	.loc stdlib.sol, 558
	PUSH S2
	EQINT 127
	PUSHCONT {
		.loc stdlib.sol, 559
		NEWC
		.loc stdlib.sol, 560
		PUSH S4
		PAIR
		POP S4
		.loc stdlib.sol, 0
	}
	IF
	.loc stdlib.sol, 0
}
WHILE
BLKDROP 3
.loc stdlib.sol, 563
DUP
FIRST
.loc stdlib.sol, 564
PUSHCONT {
	OVER
	SECOND
	ISNULL
	NOT
}
PUSHCONT {
	.loc stdlib.sol, 565
	OVER
	SECOND
	DUP
	ISNULL
	THROWIF 63
	POP S2
	.loc stdlib.sol, 566
	OVER
	FIRST
	.loc stdlib.sol, 567
	STBREF
	.loc stdlib.sol, 0
}
WHILE
.loc stdlib.sol, 570
ENDC
NIP
.loc stdlib.sol, 0

.globl	__toUpperCase
.type	__toUpperCase, @function
CALL $__toUpperCase_macro$

.macro __toUpperCase_macro
.loc stdlib.sol, 574
NEWC
NULL
PAIR
.loc stdlib.sol, 575
PUSHINT 0
.loc stdlib.sol, 576
ROT
CTOS
NULL
PUSHCONT {
	OVER
	SEMPTY
	NOT
}
PUSHCONT {
	OVER
	LDUQ 8
	PUSHCONT {
		PLDREF
		CTOS
		LDU 8
	}
	IFNOT
	POP S3
	NIP
	.loc stdlib.sol, 577
	BLKPUSH 2, 0
	.loc stdlib.sol, 578
	GTINT 96
	OVER
	LESSINT 123
	AND
	PUSHCONT {
		.loc stdlib.sol, 579
		ADDCONST -32
		.loc stdlib.sol, 0
	}
	IF
	.loc stdlib.sol, 581
	PUSH2 S4, S4
	FIRST
	XCHG S1, S2
	STU 8
	SETINDEX 0
	POP S4
	.loc stdlib.sol, 582
	PUSH S2
	INC
	POP S3
	.loc stdlib.sol, 583
	PUSH S2
	EQINT 127
	PUSHCONT {
		.loc stdlib.sol, 584
		NEWC
		.loc stdlib.sol, 585
		PUSH S4
		PAIR
		POP S4
		.loc stdlib.sol, 0
	}
	IF
	.loc stdlib.sol, 0
}
WHILE
BLKDROP 3
.loc stdlib.sol, 588
DUP
FIRST
.loc stdlib.sol, 589
PUSHCONT {
	OVER
	SECOND
	ISNULL
	NOT
}
PUSHCONT {
	.loc stdlib.sol, 590
	OVER
	SECOND
	DUP
	ISNULL
	THROWIF 63
	POP S2
	.loc stdlib.sol, 591
	OVER
	FIRST
	.loc stdlib.sol, 592
	STBREF
	.loc stdlib.sol, 0
}
WHILE
.loc stdlib.sol, 595
ENDC
NIP
.loc stdlib.sol, 0

.globl	stateInitHash
.type	stateInitHash, @function
CALL $stateInitHash_macro$

.macro stateInitHash_macro
.loc stdlib.sol, 599
NEWC
.loc stdlib.sol, 601
STSLICECONST x020134
.loc stdlib.sol, 613
ROT
STUR 16
.loc stdlib.sol, 614
STU 16
.loc stdlib.sol, 616
ROT
STUR 256
.loc stdlib.sol, 617
STU 256
.loc stdlib.sol, 618
ENDC
CTOS
SHA256U
.loc stdlib.sol, 0

"""
