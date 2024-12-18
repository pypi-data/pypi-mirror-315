#pragma once

#include "macros.h"
#include <QScrollArea>

class ScintillaEditBase;
class BScintillaEditPrivate;

class BINDINGS_API BScintillaEdit: public QScrollArea
{
    Q_OBJECT

    Q_PROPERTY(bool lineEndVisible READ lineEndVisible WRITE setLineEndVisible NOTIFY lineEndVisibleChanged)
    Q_PROPERTY(bool lineNumbersVisible READ lineNumbersVisible WRITE setLineNumbersVisible NOTIFY lineNumbersVisibleChanged)
    Q_PROPERTY(bool lineWrapped READ lineWrapped WRITE setLineWrapped NOTIFY lineWrappedChanged)
    Q_PROPERTY(bool readOnly READ readOnly WRITE setReadOnly NOTIFY readOnlyChanged FINAL)

    Q_PROPERTY(QString text READ text WRITE setText NOTIFY textChanged)

public:
    explicit BScintillaEdit(QWidget *parent = nullptr);
    virtual ~BScintillaEdit();

    bool lineEndVisible() const { return m_lineEndVisible; }
    bool lineNumbersVisible() const { return m_lineNumbersVisible; }
    bool lineWrapped() const { return m_lineWrapped; }
    bool readOnly() const { return m_readOnly; }
    const QString &text() const { return m_text; }

public slots:
    void setLineEndVisible(bool value);
    void setLineNumbersVisible(bool value);
    void setLineWrapped(bool value);
    void setReadOnly(bool value);
    void setText(const QString &value);

signals:
    void lineEndVisibleChanged(bool);
    void lineNumbersVisibleChanged(bool);
    void lineWrappedChanged(bool);
    void readOnlyChanged(bool);
    void textChanged(const QString&);

protected:
    bool m_lineEndVisible = false;
    bool m_lineNumbersVisible = false;
    bool m_lineWrapped = false;
    bool m_readOnly = false;
    QString m_text;

private:
    void setTextPrivate(const QString&value, bool setRawText);

    BScintillaEditPrivate* const d_ptr;
    Q_DECLARE_PRIVATE(BScintillaEdit)
};
