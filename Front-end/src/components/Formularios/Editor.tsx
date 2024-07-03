import React, { useState, useEffect, useRef } from "react";
import { Controlled as ControlledEditor } from 'react-codemirror2';
import 'codemirror/mode/python/python';
import 'codemirror/lib/codemirror.css';

const Editor = ({codigo, setCodigo}) => {
    const editorRef = useRef(null);
    const wrapperRef = useRef(null);

    useEffect(() => {
        setCodigo('print("Hello, World!")');
    }, []);

    const editorWillUnmount = () => {
        if (wrapperRef.current && !wrapperRef.current.hydrated) {
            editorRef.current.display.wrapper.remove();
        }
    };

    const onCodeMirrorChange = (editor, data, value) => {
        setCodigo(value);
    };
  
    return (
        <div className="editor-wrapper" ref={wrapperRef}>
            <ControlledEditor
                value={codigo}
                onBeforeChange={(editor, data, value) => onCodeMirrorChange(editor, data, value)}
                options={{
                    mode: 'python',
                    theme: 'default',
                    lineNumbers: true,
                    indentUnit: 4,
                    tabSize: 4,
                    autofocus: true,
                }}
                editorDidMount={(editor) => editorRef.current = editor}
                editorWillUnmount={editorWillUnmount}
            />
        </div>
    );
}

export default Editor;
