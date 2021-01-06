import React from 'react'

export default function Footer({children, ...restProps}){
  return <Container>{...restProps}>{children}</Container>
}

Footer.Wrapper = function FooterWrapper({children, ...restProps}){
  return <Wrapper{...restProps}>{children}</Wrapper>
}
