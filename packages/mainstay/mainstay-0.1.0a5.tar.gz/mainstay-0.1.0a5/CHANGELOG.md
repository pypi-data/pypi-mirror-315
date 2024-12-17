# Changelog

## 0.1.0-alpha.5 (2024-12-17)

Full Changelog: [v0.1.0-alpha.4...v0.1.0-alpha.5](https://github.com/mainstay-io/mainstay-python/compare/v0.1.0-alpha.4...v0.1.0-alpha.5)

### Features

* **api:** api update ([#40](https://github.com/mainstay-io/mainstay-python/issues/40)) ([36667ac](https://github.com/mainstay-io/mainstay-python/commit/36667ac08944c80aba5cc8d7c72d7d7f0ea1a004))
* **api:** api update ([#41](https://github.com/mainstay-io/mainstay-python/issues/41)) ([fd6f8cd](https://github.com/mainstay-io/mainstay-python/commit/fd6f8cd10606dcc2949a1cd28a2293c1da1fca65))
* **api:** api update ([#63](https://github.com/mainstay-io/mainstay-python/issues/63)) ([6be4a1a](https://github.com/mainstay-io/mainstay-python/commit/6be4a1ad08bf87054328ea028a1454c605172156))
* **api:** OpenAPI spec update via Stainless API ([#22](https://github.com/mainstay-io/mainstay-python/issues/22)) ([f4716c8](https://github.com/mainstay-io/mainstay-python/commit/f4716c853a3f0801b87f68aea93569fd12c9e900))
* **api:** OpenAPI spec update via Stainless API ([#24](https://github.com/mainstay-io/mainstay-python/issues/24)) ([3b6b609](https://github.com/mainstay-io/mainstay-python/commit/3b6b609e57956768eedb7bb87835ea03d8f0dcf8))


### Bug Fixes

* **client:** avoid OverflowError with very large retry counts ([#38](https://github.com/mainstay-io/mainstay-python/issues/38)) ([2a79dc1](https://github.com/mainstay-io/mainstay-python/commit/2a79dc1b5dbde0734d20e5e19d862631be31dbd8))
* **client:** compat with new httpx 0.28.0 release ([#56](https://github.com/mainstay-io/mainstay-python/issues/56)) ([b0ef1bb](https://github.com/mainstay-io/mainstay-python/commit/b0ef1bb571af61399dac2033853c39af6f7cdf87))


### Chores

* add docstrings to raw response properties ([#29](https://github.com/mainstay-io/mainstay-python/issues/29)) ([8bade40](https://github.com/mainstay-io/mainstay-python/commit/8bade405417f0b65117dc140f23b51016e46a162))
* add repr to PageInfo class ([#39](https://github.com/mainstay-io/mainstay-python/issues/39)) ([e4b6d4b](https://github.com/mainstay-io/mainstay-python/commit/e4b6d4b996ab0c7cc1ae172f450b4bb7bc3e25c8))
* **ci:** also run pydantic v1 tests ([#26](https://github.com/mainstay-io/mainstay-python/issues/26)) ([07d20ff](https://github.com/mainstay-io/mainstay-python/commit/07d20fffc6228f2502eccba21ee281ab95541b68))
* **client:** fix parsing union responses when non-json is returned ([#25](https://github.com/mainstay-io/mainstay-python/issues/25)) ([c996d8c](https://github.com/mainstay-io/mainstay-python/commit/c996d8c026679e3c20ad9ae6902c02895043e3f4))
* **internal:** add support for parsing bool response content ([#37](https://github.com/mainstay-io/mainstay-python/issues/37)) ([a660ad9](https://github.com/mainstay-io/mainstay-python/commit/a660ad9619804d52f03a7e2e248e7cfdb6ab08b9))
* **internal:** add support for TypeAliasType ([#62](https://github.com/mainstay-io/mainstay-python/issues/62)) ([83038e7](https://github.com/mainstay-io/mainstay-python/commit/83038e7b7dfb13a121574eb6aed24c4e326833c7))
* **internal:** bump pydantic dependency ([#59](https://github.com/mainstay-io/mainstay-python/issues/59)) ([08f4883](https://github.com/mainstay-io/mainstay-python/commit/08f48839910fba704386c2c5cd7a43f3342b2bcf))
* **internal:** bump pyright ([#57](https://github.com/mainstay-io/mainstay-python/issues/57)) ([bf998ca](https://github.com/mainstay-io/mainstay-python/commit/bf998ca41db02b9bd7419518028a427b0b3cc660))
* **internal:** bump pyright ([#61](https://github.com/mainstay-io/mainstay-python/issues/61)) ([aa9fd58](https://github.com/mainstay-io/mainstay-python/commit/aa9fd58da6f5fad55510593b894e2ff85872ebe1))
* **internal:** bump pyright / mypy version ([#33](https://github.com/mainstay-io/mainstay-python/issues/33)) ([5ecd312](https://github.com/mainstay-io/mainstay-python/commit/5ecd31253e2ec9bf285ecd487cf0d707bfbdd4d3))
* **internal:** bump ruff ([#32](https://github.com/mainstay-io/mainstay-python/issues/32)) ([c714557](https://github.com/mainstay-io/mainstay-python/commit/c714557340bd5ab1dd3adaef3e9740209a6706ef))
* **internal:** codegen related update ([#31](https://github.com/mainstay-io/mainstay-python/issues/31)) ([e320a0b](https://github.com/mainstay-io/mainstay-python/commit/e320a0ba20616acfe1e52d69add23a6606d29943))
* **internal:** codegen related update ([#34](https://github.com/mainstay-io/mainstay-python/issues/34)) ([115e9df](https://github.com/mainstay-io/mainstay-python/commit/115e9dffaf1919803d4dae06ee715329c9b82b9e))
* **internal:** codegen related update ([#35](https://github.com/mainstay-io/mainstay-python/issues/35)) ([9aad407](https://github.com/mainstay-io/mainstay-python/commit/9aad4072a08d06709d2ca92e322726591c46bbc9))
* **internal:** codegen related update ([#36](https://github.com/mainstay-io/mainstay-python/issues/36)) ([e778d96](https://github.com/mainstay-io/mainstay-python/commit/e778d96c9344e30d26e58f4390dd60a4f1701d4c))
* **internal:** codegen related update ([#54](https://github.com/mainstay-io/mainstay-python/issues/54)) ([8d3e441](https://github.com/mainstay-io/mainstay-python/commit/8d3e4419ef6fb66347dc86cc637b6bc66c4bc074))
* **internal:** codegen related update ([#55](https://github.com/mainstay-io/mainstay-python/issues/55)) ([827fd58](https://github.com/mainstay-io/mainstay-python/commit/827fd58fd65ca60f44d9429f36113809be347255))
* **internal:** fix compat model_dump method when warnings are passed ([#52](https://github.com/mainstay-io/mainstay-python/issues/52)) ([87753e1](https://github.com/mainstay-io/mainstay-python/commit/87753e1f7694ff135fe0d3eab01a5e7daeb0d5a1))
* **internal:** use different 32bit detection method ([#23](https://github.com/mainstay-io/mainstay-python/issues/23)) ([2543e59](https://github.com/mainstay-io/mainstay-python/commit/2543e592fe2f010300ec627f3546136868f9de98))
* **internal:** version bump ([#20](https://github.com/mainstay-io/mainstay-python/issues/20)) ([2f51381](https://github.com/mainstay-io/mainstay-python/commit/2f513815237ee8eb057b8ef07b3f4ebfb69d3724))
* make the `Omit` type public ([#58](https://github.com/mainstay-io/mainstay-python/issues/58)) ([91aa7ae](https://github.com/mainstay-io/mainstay-python/commit/91aa7aeb76c5f608a58760a58876d3f758351f95))
* pyproject.toml formatting changes ([#28](https://github.com/mainstay-io/mainstay-python/issues/28)) ([70d893a](https://github.com/mainstay-io/mainstay-python/commit/70d893a160d73267060b17bc06effd2f6462cdd8))
* rebuild project due to codegen change ([#42](https://github.com/mainstay-io/mainstay-python/issues/42)) ([74f0a29](https://github.com/mainstay-io/mainstay-python/commit/74f0a298393faf292a3ff00755e1931e19f175f7))
* rebuild project due to codegen change ([#43](https://github.com/mainstay-io/mainstay-python/issues/43)) ([987ace3](https://github.com/mainstay-io/mainstay-python/commit/987ace3ab6c9b30f71fae2b0440b8e314ef3403c))
* rebuild project due to codegen change ([#44](https://github.com/mainstay-io/mainstay-python/issues/44)) ([e15f71d](https://github.com/mainstay-io/mainstay-python/commit/e15f71da1298975ca773b434a1533b01891b2a14))
* rebuild project due to codegen change ([#45](https://github.com/mainstay-io/mainstay-python/issues/45)) ([d2c7122](https://github.com/mainstay-io/mainstay-python/commit/d2c7122a0cf138cf2deac02dc176c921441f4008))
* rebuild project due to codegen change ([#46](https://github.com/mainstay-io/mainstay-python/issues/46)) ([e990905](https://github.com/mainstay-io/mainstay-python/commit/e9909050731b4598baa7a81a0c93905d6353542e))
* rebuild project due to codegen change ([#47](https://github.com/mainstay-io/mainstay-python/issues/47)) ([d6ab7b4](https://github.com/mainstay-io/mainstay-python/commit/d6ab7b40f8316fc13f52246c9a3df78665733e6c))
* rebuild project due to codegen change ([#48](https://github.com/mainstay-io/mainstay-python/issues/48)) ([21a91a4](https://github.com/mainstay-io/mainstay-python/commit/21a91a4f545dfc41895642f7df359fca1b47d5ed))
* rebuild project due to codegen change ([#49](https://github.com/mainstay-io/mainstay-python/issues/49)) ([6a9fe31](https://github.com/mainstay-io/mainstay-python/commit/6a9fe317d9c68f88e4a4e907916fba52bbac9059))
* rebuild project due to codegen change ([#50](https://github.com/mainstay-io/mainstay-python/issues/50)) ([fc4ea9e](https://github.com/mainstay-io/mainstay-python/commit/fc4ea9e2bf6eeaff9886ba5b82dbf7a5f599be9a))
* rebuild project due to codegen change ([#51](https://github.com/mainstay-io/mainstay-python/issues/51)) ([12db39a](https://github.com/mainstay-io/mainstay-python/commit/12db39a1c3947a4ccf847640b1da7a8dcc849f72))


### Documentation

* add info log level to readme ([#53](https://github.com/mainstay-io/mainstay-python/issues/53)) ([d481c14](https://github.com/mainstay-io/mainstay-python/commit/d481c1483c37675278f4b1ef678f72e5117bca16))
* **readme:** add section on determining installed version ([#30](https://github.com/mainstay-io/mainstay-python/issues/30)) ([1841ede](https://github.com/mainstay-io/mainstay-python/commit/1841edecdb4958bf0cb4d3c34b23bf6b09a08a14))
* **readme:** fix http client proxies example ([#60](https://github.com/mainstay-io/mainstay-python/issues/60)) ([69bfe9d](https://github.com/mainstay-io/mainstay-python/commit/69bfe9d6e77b0ad38676deeec95ac864d8135658))

## 0.1.0-alpha.4 (2024-08-14)

Full Changelog: [v0.1.0-alpha.3...v0.1.0-alpha.4](https://github.com/mainstay-io/mainstay-python/compare/v0.1.0-alpha.3...v0.1.0-alpha.4)

### Features

* add parallelized calls code ([91f3c4c](https://github.com/mainstay-io/mainstay-python/commit/91f3c4cdd62befe8f1407e7fc0171540fede450e))
* added crime and school parallelized calls ([7edfa2e](https://github.com/mainstay-io/mainstay-python/commit/7edfa2eec3556edb72f85fa36742c37b17cd4a72))
* clean up on top of the diffs + questions ([ebef7e7](https://github.com/mainstay-io/mainstay-python/commit/ebef7e7b65092f6bd7b6932428ac65b44b1b60e4))
* copied changes ([76364b7](https://github.com/mainstay-io/mainstay-python/commit/76364b79a730c71eb119551c445fd92516a62edf))
* fix imports ([1165409](https://github.com/mainstay-io/mainstay-python/commit/11654099fb2e5c0eccd4f37c3dc10f2b763eb6c9))
* fix names ([f96c489](https://github.com/mainstay-io/mainstay-python/commit/f96c489241b9e1c4da39a33b6bfa4082a71382de))
* fixed examples files linting ([26c4a60](https://github.com/mainstay-io/mainstay-python/commit/26c4a60deabe2bb7b5a621199ed6a7c97167875d))
* revert all the accidental custom codes, keep only the parallelized calls ([bb045b7](https://github.com/mainstay-io/mainstay-python/commit/bb045b7770017fb08891845a436c826e5f9310f5))

## 0.1.0-alpha.3 (2024-08-13)

Full Changelog: [v0.1.0-alpha.2...v0.1.0-alpha.3](https://github.com/mainstay-io/mainstay-python/compare/v0.1.0-alpha.2...v0.1.0-alpha.3)

### Features

* **api:** manual updates ([#15](https://github.com/mainstay-io/mainstay-python/issues/15)) ([6b3e125](https://github.com/mainstay-io/mainstay-python/commit/6b3e125658144d4f687bb9ccfa6dd9eedaa57624))
* **api:** OpenAPI spec update via Stainless API ([#16](https://github.com/mainstay-io/mainstay-python/issues/16)) ([8a2263a](https://github.com/mainstay-io/mainstay-python/commit/8a2263a1b99f3dc3cde7c96a64ea1f6da9273ce3))


### Chores

* **examples:** minor formatting changes ([#10](https://github.com/mainstay-io/mainstay-python/issues/10)) ([ccf2d18](https://github.com/mainstay-io/mainstay-python/commit/ccf2d18a1c89a3dd1e2104de4e9a1a5ddefcd888))
* **internal:** codegen related update ([#13](https://github.com/mainstay-io/mainstay-python/issues/13)) ([69c2224](https://github.com/mainstay-io/mainstay-python/commit/69c222485cc5a0580b51b13609f8a503e8bfb5e9))
* **internal:** version bump ([#11](https://github.com/mainstay-io/mainstay-python/issues/11)) ([b584ac1](https://github.com/mainstay-io/mainstay-python/commit/b584ac161dc6915e58e6fc161e06604985c1ad40))

## 0.1.0-alpha.2 (2024-08-10)

Full Changelog: [v0.1.0-alpha.1...v0.1.0-alpha.2](https://github.com/mainstay-io/mainstay-python/compare/v0.1.0-alpha.1...v0.1.0-alpha.2)

### Chores

* **ci:** bump prism mock server version ([#6](https://github.com/mainstay-io/mainstay-python/issues/6)) ([1f9d7f8](https://github.com/mainstay-io/mainstay-python/commit/1f9d7f817d34419f9603c25f1206678706db5e57))
* **internal:** ensure package is importable in lint cmd ([#8](https://github.com/mainstay-io/mainstay-python/issues/8)) ([c49ec2b](https://github.com/mainstay-io/mainstay-python/commit/c49ec2b58d18671eaea432058367f95645ec3d39))

## 0.1.0-alpha.1 (2024-08-10)

Full Changelog: [v0.0.1-alpha.0...v0.1.0-alpha.1](https://github.com/mainstay-io/mainstay-python/compare/v0.0.1-alpha.0...v0.1.0-alpha.1)

### Features

* **api:** OpenAPI spec update via Stainless API ([9cd559e](https://github.com/mainstay-io/mainstay-python/commit/9cd559e96e2d154346a17d225bdea3a3ad3d78b6))
* **api:** OpenAPI spec update via Stainless API ([ab54c3c](https://github.com/mainstay-io/mainstay-python/commit/ab54c3c0b590cd2197359984da5242bfebe2ebe8))


### Chores

* go live ([#2](https://github.com/mainstay-io/mainstay-python/issues/2)) ([e8fb3e5](https://github.com/mainstay-io/mainstay-python/commit/e8fb3e5bc68c7b4fc331e9ac9fba91d7a8bf0120))
