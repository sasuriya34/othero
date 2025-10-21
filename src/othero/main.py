def main(argv=None):
    """シンプルなエントリポイント。"""
    import sys
    argv = argv if argv is not None else sys.argv[1:]
    if argv and argv[0] in ("-h", "--help"):
        print("usage: othero [hello]")
        return 0
    # デフォルトの動作
    print("Hello from othero!")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
